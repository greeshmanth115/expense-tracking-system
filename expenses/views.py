from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Sum, Count
from django.utils import timezone
from itertools import chain
from .models import Expense, Income, CATEGORY_CHOICES, INCOME_SOURCE_CHOICES
from .forms import ExpenseForm, IncomeForm, SignUpForm


@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)
    today = timezone.now().date()

    total_expense = expenses.aggregate(Sum("amount"))["amount__sum"] or 0
    total_income = incomes.aggregate(Sum("amount"))["amount__sum"] or 0
    balance = total_income - total_expense

    month_expense = expenses.filter(date__year=today.year, date__month=today.month).aggregate(Sum("amount"))["amount__sum"] or 0
    month_income = incomes.filter(date__year=today.year, date__month=today.month).aggregate(Sum("amount"))["amount__sum"] or 0

    by_category = list(
        expenses.values("category").annotate(total=Sum("amount"), n=Count("id")).order_by("-total")
    )
    max_cat_total = max([c["total"] for c in by_category], default=0)
    category_map = dict(CATEGORY_CHOICES)
    for c in by_category:
        c["label"] = category_map.get(c["category"], c["category"])
        c["pct"] = int((c["total"] / max_cat_total) * 100) if max_cat_total else 0

    recent_expenses = expenses[:5]
    recent_income = incomes[:5]

    return render(request, "expenses/dashboard.html", {
        "total_expense": total_expense, "total_income": total_income, "balance": balance,
        "month_expense": month_expense, "month_income": month_income,
        "by_category": by_category, "recent_expenses": recent_expenses, "recent_income": recent_income,
    })


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    category = request.GET.get("category")
    if category:
        expenses = expenses.filter(category=category)
    total = expenses.aggregate(Sum("amount"))["amount__sum"] or 0
    return render(request, "expenses/expense_list.html", {
        "expenses": expenses, "total": total,
        "categories": CATEGORY_CHOICES,
        "selected_category": category,
    })


@login_required
def expense_add(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm()
    return render(request, "expenses/expense_form.html", {"form": form, "title": "Add Expense"})


@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "expenses/expense_form.html", {"form": form, "title": "Edit Expense"})


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        expense.delete()
        return redirect("expense_list")
    return render(request, "expenses/expense_confirm_delete.html", {"obj": expense, "back": "expense_list"})


@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user)
    source = request.GET.get("source")
    if source:
        incomes = incomes.filter(source=source)
    total = incomes.aggregate(Sum("amount"))["amount__sum"] or 0
    return render(request, "expenses/income_list.html", {
        "incomes": incomes, "total": total,
        "sources": INCOME_SOURCE_CHOICES,
        "selected_source": source,
    })


@login_required
def income_add(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect("income_list")
    else:
        form = IncomeForm()
    return render(request, "expenses/income_form.html", {"form": form, "title": "Add Income"})


@login_required
def income_edit(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect("income_list")
    else:
        form = IncomeForm(instance=income)
    return render(request, "expenses/income_form.html", {"form": form, "title": "Edit Income"})


@login_required
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == "POST":
        income.delete()
        return redirect("income_list")
    return render(request, "expenses/expense_confirm_delete.html", {"obj": income, "back": "income_list"})


@login_required
def report(request):
    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)

    total_expense = expenses.aggregate(Sum("amount"))["amount__sum"] or 0
    total_income = incomes.aggregate(Sum("amount"))["amount__sum"] or 0
    balance = total_income - total_expense

    exp_by_category = list(
        expenses.values("category").annotate(total=Sum("amount")).order_by("-total")
    )
    category_map = dict(CATEGORY_CHOICES)
    for c in exp_by_category:
        c["label"] = category_map.get(c["category"], c["category"])
        c["pct"] = int((c["total"] / total_expense) * 100) if total_expense else 0

    inc_by_source = list(
        incomes.values("source").annotate(total=Sum("amount")).order_by("-total")
    )
    source_map = dict(INCOME_SOURCE_CHOICES)
    for s in inc_by_source:
        s["label"] = source_map.get(s["source"], s["source"])
        s["pct"] = int((s["total"] / total_income) * 100) if total_income else 0

    exp_rows = [{"date": e.date, "title": e.title, "type": "Expense", "category": e.get_category_display(), "amount": -e.amount} for e in expenses]
    inc_rows = [{"date": i.date, "title": i.title, "type": "Income", "category": i.get_source_display(), "amount": i.amount} for i in incomes]
    transactions = sorted(chain(exp_rows, inc_rows), key=lambda r: r["date"], reverse=True)

    return render(request, "expenses/report.html", {
        "total_expense": total_expense, "total_income": total_income, "balance": balance,
        "exp_by_category": exp_by_category, "inc_by_source": inc_by_source,
        "transactions": transactions,
    })


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(request, "expenses/signup.html", {"form": form})
