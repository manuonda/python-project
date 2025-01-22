from dataclasses import dataclass
from pydantic import BaseModel, Field

from pydantic_ai import Agent, RunContext


class DatabaseConn:
    """ This is fake base connection """

    @classmethod
    async def customer_name(cls, * , id: int) -> str | None:
        if id == 123 :
             return 'Jhon'
        
    @classmethod
    async def customer_balance(cls, * , id: int , include_pending: bool) -> float | None:
        if id == 123 :
             return 123.45
        else:
            raise ValueError('Customer not found')
    
@dataclass
class SupportDependencies:
    customer_id: int 
    db: DatabaseConn


class SupportResult(BaseModel):
    support_advice: str = Field(description = 'Advice returned to the customer')
    block_card: bool = Field(description = 'Whether to block their')
    risk: int = Field(description =  'Risk level of the customer', ge = 0, le = 10)



support_agent =  Agent(
    model="openai:gpt-4o-mini",
    deps_type=SupportDependencies,
    result_type=SupportResult,
    system_prompt=(
        "You are a support agent in our bank, give the"
        "customer support and jugde the risk level of their query"
        "Reply using the customer's name"
    )
)

@support_agent.system_prompt
async def get_customer_name(ctx: RunContext[SupportDependencies]) -> str:
    """ Get the customer name """
    customer_name = ctx.deps.db.customer_name(id = ctx.deps.customer_id)
    return f"The customer name is {customer_name}"

@support_agent.tool
async def customer_balance(ctx: RunContext[SupportDependencies] , include_pending: bool) -> str:
    """ Return the customer's current account balance """
    balance = ctx.deps.db.customer_balance( id = ctx.deps.customer_id,
                                           include_pending= include_pending)
    
    return f'${balance: .2f}'


