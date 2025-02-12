from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, ForwardRef


# Forward reference for Event
Event = ForwardRef("Event")


class BudgetPlan(SQLModel, table=True):
    """
    Represents the planning phase for an event group.
    """
    __tablename__ = "budget_plans"
 
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    total_budget: float = Field(nullable=False)  # Total budget allocated for all events in this group
    name: str = Field(nullable=False, max_length=255)  # Name of the event group (e.g., "Wedding", "Conference")
    description: Optional[str] = Field(default=None, max_length=500)  # Optional description of the budget plan

    # Relationship to event budgets
    event_budgets: List["EventBudget"] = Relationship(back_populates="budget_plan")


class EventBudget(SQLModel, table=True):
    """
    Represents the planned budget for a specific event.
    """
    __tablename__ = "event_budgets"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    budget_plan_id: int = Field(foreign_key="budget_plans.id", nullable=False)
    event_id: int = Field(foreign_key="events.id", nullable=False)
    allocated_amount: float = Field(nullable=False)  # Amount allocated for this event
    description: Optional[str] = Field(default=None, max_length=500)  # Description or notes on the allocation

    # Relationship to budget plan
    budget_plan: Optional["BudgetPlan"] = Relationship(back_populates="event_budgets")

    # Relationship to event
    event: Optional["Event"] = Relationship(back_populates="event_budget")


class Expense(SQLModel, table=True):
    """
    Represents the actual expenses tracked for an event.
    """
    __tablename__ = "expenses"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    event_id: int = Field(foreign_key="events.id", nullable=False)
    description: str = Field(nullable=False, max_length=255)  # Description of the expense
    amount: float = Field(nullable=False)  # Expense amount
    date: Optional[str] = Field(default=None)  # Date of the expense (could use datetime)

    # Relationship to event
    event: Optional["Event"] = Relationship(back_populates="expenses")


class ExpenseAnalysis(SQLModel, table=True):
    """
    Represents analysis of expenses for an event.
    """
    __tablename__ = "expense_analysis"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    event_id: int = Field(foreign_key="events.id", nullable=False)
    planned_budget: float = Field(nullable=False)  # Total planned budget for the event
    actual_expense: float = Field(nullable=False)  # Total actual expense for the event
    variance: float = Field(nullable=False)  # Difference between planned and actual expense
    notes: Optional[str] = Field(default=None, max_length=500)  # Optional notes or insights on the analysis

    # Relationship to event
    event: Optional["Event"] = Relationship(back_populates="expense_analysis")


class Event(SQLModel, table=True):
    """
    Represents an event, linked to budgets, expenses, and analysis.
    """
    __tablename__ = "events"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(nullable=False, max_length=255)  # Name of the event
    date: Optional[str] = Field(default=None)  # Optional: Event date, could use datetime for real-world scenarios

    # Relationships
    event_budget: Optional["EventBudget"] = Relationship(back_populates="event")
    expenses: List["Expense"] = Relationship(back_populates="event")
    expense_analysis: Optional["ExpenseAnalysis"] = Relationship(back_populates="event")
