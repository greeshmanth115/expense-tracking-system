from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ("food", "🍔 Food"),
    ("transport", "🚗 Transport"),
    ("shopping", "🛍️ Shopping"),
    ("bills", "🧾 Bills"),
    ("health", "💊 Health"),
    ("other", "📦 Other"),
]

PAYMENT_CHOICES = [
    ("cash", "Cash"),
    ("card", "Card"),
    ("upi", "UPI"),
    ("bank", "Bank Transfer"),
]

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="cash")
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True, help_text="Short details about this expense")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.title} - {self.amount}"


INCOME_SOURCE_CHOICES = [
    ("salary", "💼 Salary"),
    ("freelance", "🧑‍💻 Freelance"),
    ("business", "🏪 Business"),
    ("investment", "📈 Investment"),
    ("gift", "🎁 Gift"),
    ("other", "📦 Other"),
]

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=20, choices=INCOME_SOURCE_CHOICES, default="salary")
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.title} - {self.amount}"
