from pydantic import BaseModel, Field
from statum.actions import Action
from typing import List
from statum.LLMs.openai_function import openai_function


system_prompt = """You are a contracted product manager for a startup that is building a new product. You have been tasked with creating a Product Review Document (PRD) for a new product based on a given description"""

TASK = """Create a Product Review Document (PRD) for a new product based on the following description: %s

for %s : %s
"""
problem_statement = """The problem statement is the first section of the PRD. It should be a short, concise description of the problem that the product is trying to solve. It should be written in plain language that anyone can understand.
The problem statement should answe the following questions:
- What is the people/customer problem we're trying to solve? (i.e., what is the overaching Job to be Done, and why does that matter to customers?)
- What is the business problem we're trying to solve?
~Comments:
> This is where the reader should be able to quickly understand why working on this is so important for your audience, product and for the business.
> Connect the problem to the companies strategy and business lines.
> THe sum of this section should have a strong opionion-based POV on why this direction will influence how we'll achieve the companies strategic goals.
"""

hypothesis = """The hypothesis is the second section of the PRD. It should be a short, concise description of the problem that the product is trying to solve. It should be written in plain language that anyone can understand.
It should contain the why, what, and how of the product.
The hypothesis should answe the following questions:
Why: Establishes causality by laying out how the solution will address the problem.
What: What do you believe is true and what do you will happen if you are correct? Frame your hypothesis in a customer-centric way, while also focusing on how the proposed solution will solve the business problem.
~Example: We believe that between account creation and profile setup in the onboarding funnel members are confused about what to do next, ultimately abandoning the onboarding funnel. We believe confusion stems from [poor layout / hidden CTA / etc ], whihc if remedied would improve activation rates."""

expected_outcomes = """An outcome in product development refers to the result of impact that a product or feature has on the user of business. It is measurable and observable change that can be attributed to the product or feature. Examples of outcomes include increased user engagement, decreased churn rate, and increased revenue. Outcomes are important in product development as they help to ensure that the product is meeting the needs and goals of the users and business"""

learning_goals = """A learning goal could be to better understand how users are interacting with the product, to identify areas where improvements can be made, or to gather feedback on a specific features or aspects of the product.
It's important to have a clear idea of what you want to learn, and to have a plan in place for gathering and analyzing data, in order to achieve your learning goals."""

metrics = """Why: Ensures your feature's impact can be measured
What: Given your hypothesis, what KPIs are you looking to impact and why?
KPIs: Try to have only 1-3 primary KPIs to make reporting to stakeholders simpler and easier to understand
Metrics that matter: the secondary metrics are for additional context, insight, to explore new opportunities and risks."""

potential_risks = """Think pre-mortem - imagine that the project has failed, and then work backward to determine what potentially could lead to the failure of the project"""

technical_gameplan = """Create a list of tasks required by the engineering team to build the product"""

class Task_CreatePRD(BaseModel):
    problem_statement: str = Field(..., description=problem_statement)
    hypothesis: str = Field(..., description=hypothesis)
    expected_outcomes: str = Field(description=expected_outcomes)
    learning_goals: str = Field(..., description=learning_goals)
    metrics: str = Field(..., description=metrics)
    potential_risks: str = Field(..., description=potential_risks)
    technical_gameplan: List[str] = Field(..., description=technical_gameplan)

class CreatePRD(Action):
    
    def __init__(self, response_model: BaseModel = Task_CreatePRD, system_prompt: str = system_prompt):
        super().__init__()
        self.system_prompt = system_prompt
        self.response_model = response_model
        self.LLM = openai_function
    

    def forward(self, query: str, company_name:str, company_description:str):
        query = TASK % (query, company_description, company_name)
        response = self.LLM(query=query, responseModel=self.response_model, system_prompt=self.system_prompt)
        return response