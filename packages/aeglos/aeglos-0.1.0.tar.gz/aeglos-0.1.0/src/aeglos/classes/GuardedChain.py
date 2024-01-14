from langchain_core.beta.runnables.context import config_with_context
from langchain_core.load.dump import dumpd
from langchain_core.runnables.config import (
    RunnableConfig,
    ensure_config,
    get_callback_manager_for_config,
    get_async_callback_manager_for_config,
    patch_config,
    get_config_list,
    get_executor_for_config
)
from langchain_core.messages import HumanMessage
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.runnables.utils import (
    Output,
    Input,
    gather_with_concurrency
)
from typing import (
    cast,
    Any,
    List,
    Union,
)
from langchain_core.beta.runnables.context import aconfig_with_context

from ..interfaces.GlobalMessages import malicious_input_found_message, check_unable
from .PromptChecker.PromptChecker import PromptChecker 


def guard_chain(chain:Any)->Any:
    """
    takes a chain, and returns it's guarded counterpart. This new chain should be used instead of the original chain.
    GuardedChain also declared here
    """
    class GuardedChain(chain.__class__):
        prompt_checker = PromptChecker() 
        
        # HELPER FUNCTIONS BELOW---------------- 
        def runnable_invoke(self, *args, **kwargs):
            "This function is called when the class is of type runnable"
            input = args[0] if args else None
            config = args[1] if len(args) > 1 else kwargs.get('config', None)
            # setup callbacks and context
            config = config_with_context(ensure_config(config), self.steps)
            callback_manager = get_callback_manager_for_config(config)
            # start the root run
            run_manager = callback_manager.on_chain_start(
                dumpd(self), input, name=config.get("run_name") or self.get_name()
            )
            
            # invoke all steps in sequence
            try:
                found_malicious=False
                for i, step in enumerate(self.steps):
                    if isinstance(input,ChatPromptValue) :
                        # iterate thorough all the messages
                        for message in input.messages: #### functionize
                            # if its a message and error message inf
                            if isinstance(message,HumanMessage):
                                if malicious_input_found_message in message.content or self.prompt_checker.concurrent_contains_known_attack(message.content): 
                                    found_malicious=True
                                    
                                    # debugging--------
                                    if malicious_input_found_message not in message.content:
                                        print("tool called on "+message.content)
                                    break
                    # if malicious- break
                    if found_malicious:
                        break
                    input = step.invoke(
                        input,
                        # mark each step as a child run
                        patch_config(
                            config, callbacks=run_manager.get_child(f"seq:step:{i+1}"),
                        )
                    )
                    
            # finish the root run
            except BaseException as e:
                run_manager.on_chain_error(e)
                raise
            else:
                final_val=input if not found_malicious else malicious_input_found_message
                run_manager.on_chain_end(final_val)

                # if malicious, return error message
                return cast(Output, final_val)

        async def runnable_ainvoke(self, *args, **kwargs) -> Output:
            # Assuming the first argument is 'input' and the second is 'config'
            input = args[0] if args else None
            config = args[1] if len(args) > 1 else kwargs.get('config', None)

            # Include any additional keyword arguments in the config
            if kwargs:
                config = {**config, **kwargs} if config is not None else kwargs

            # setup callbacks and context
            config = aconfig_with_context(ensure_config(config), self.steps)
            callback_manager = get_async_callback_manager_for_config(config)
            # start the root run
            run_manager = await callback_manager.on_chain_start(
                dumpd(self), input, name=config.get("run_name") or self.get_name()
            )

            # invoke all steps in sequence
            try:
                found_malicious=False
                for i, step in enumerate(self.steps):
                    if isinstance(input,ChatPromptValue):
                        for message in input.messages: #### functionize
                            # if its a message and error message inf
                            if isinstance(message,HumanMessage):
                                if malicious_input_found_message in message.content or self.prompt_checker.concurrent_contains_known_attack(message.content): 
                                    found_malicious=True
                                    # debugging--------
                                    if malicious_input_found_message not in message.content:
                                        print("tool called on "+message.content)
                                    break
                    if found_malicious:
                        break
                    input = await step.ainvoke(
                        input,
                        # mark each step as a child run
                        patch_config(
                            config, callbacks=run_manager.get_child(f"seq:step:{i+1}")
                        ),
                    )
            # finish the root run
            except BaseException as e:
                await run_manager.on_chain_error(e)
                raise
            else:
                final_val=input if not found_malicious else malicious_input_found_message
                await run_manager.on_chain_end(final_val)
                return cast(Output, final_val)

        def runnable_batch(
            self,
            *args,
            return_exceptions: bool = False,
            **kwargs,
        ) -> List[Output]:
            """
            Default implementation runs invoke in parallel using a thread pool executor.

            The default implementation of batch works well for IO bound runnables.

            Subclasses should override this method if they can batch more efficiently;
            e.g., if the underlying runnable uses an API which supports a batch mode.
            """
            # Extract inputs and config from args, assuming they are the first two arguments
            inputs = args[0] if args else []
            config = args[1] if len(args) > 1 else kwargs.get('config', None)

            if not inputs:
                return []

            configs = get_config_list(config, len(inputs))

            def batch_invoke(input: Input, config: RunnableConfig) -> Union[Output, Exception]:
                if return_exceptions:
                    try:
                        return self.invoke(input, config, **kwargs)
                    except Exception as e:
                        return e
                else:
                    return self.invoke(input, config, **kwargs)

            # If there's only one input, don't bother with the executor
            if len(inputs) == 1:
                return cast(List[Output], [batch_invoke(inputs[0], configs[0])])

            with get_executor_for_config(configs[0]) as executor:
                return cast(List[Output], list(executor.map(batch_invoke, inputs, configs)))

        async def runnable_abatch(self, *args, return_exceptions: bool = False, **kwargs) -> List[Output]:
            """
            Default implementation runs ainvoke in parallel using asyncio.gather.

            The default implementation of batch works well for IO bound runnables.

            Subclasses should override this method if they can batch more efficiently;
            e.g., if the underlying runnable uses an API which supports a batch mode.
            """
            # Extract inputs and config from args, assuming they are the first two arguments
            inputs = args[0] if args else []
            config = args[1] if len(args) > 1 else kwargs.get('config', None)

            if not inputs:
                return []

            configs = get_config_list(config, len(inputs))

            async def abatch_ainvoke(input: Input, config: RunnableConfig) -> Union[Output, Exception]:
                if return_exceptions:
                    try:
                        return await self.ainvoke(input, config, **kwargs)
                    except Exception as e:
                        return e
                else:
                    return await self.ainvoke(input, config, **kwargs)

            coros = map(abatch_ainvoke, inputs, configs)
            return await gather_with_concurrency(configs[0].get("max_concurrency"), *coros)

        # MAIN FUNCTIONS BELOW---------------- 
        def invoke(self, *args, **kwargs):
            try:
                return self.runnable_invoke(*args,**kwargs)
            except:
                print(check_unable)
                return super().invoke(*args, **kwargs)
        
        async def ainvoke(self, *args, **kwargs):
            try:
                return await self.runnable_ainvoke(*args,**kwargs)
            except Exception as e:
                print(check_unable)
                return await super().ainvoke(*args, **kwargs)
            
        def batch(self, *args, **kwargs):
            try:
                return  self.runnable_batch(*args,**kwargs)
            except Exception as e:
                print(e)
                return super().batch(*args, **kwargs)
        
        async def abatch(self, *args, **kwargs):
            try:
                return await self.runnable_abatch(*args,**kwargs)
            except:
                print(check_unable)
                return await super().abatch(*args, **kwargs)
        
        def stream(
            self, *args, **kwargs):
            """
            Default implementation of stream, which calls invoke.
            Subclasses should override this method if they support streaming output.
            """
            yield self.invoke(*args, **kwargs)

        async def astream(
            self, *args, **kwargs
        ):
            """
            Default implementation of astream, which calls ainvoke.
            Subclasses should override this method if they support streaming output.
            """
            yield await self.ainvoke(*args, **kwargs)

    
    return GuardedChain(chain)