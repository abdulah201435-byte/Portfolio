from django.db import models

ICON_CHOICES = [
    ("code", "Code"), ("py", "Python"), ("stack", "Stack"),
    ("flow", "Workflow"), ("bot", "AI bot"), ("db", "Database"),
]


class Service(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField(max_length=300)
    icon = models.CharField(max_length=10, choices=ICON_CHOICES, default="code")
    order = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=60)
    cat = models.CharField("Category", max_length=60)
    icon = models.CharField(max_length=10, choices=ICON_CHOICES, default="code")
    desc = models.CharField("Description", max_length=200)
    order = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=60, default="Frontend Development")
    technologies = models.CharField(max_length=300, blank=True, help_text="Separate with commas, e.g. HTML, CSS, n8n")
    frontend = models.TextField(blank=True)
    backend = models.TextField(blank=True)
    integrations = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=40, blank=True)
    image = models.ImageField(upload_to="projects/", blank=True)
    live_url = models.URLField(blank=True)
    source_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "-date", "id"]

    def __str__(self):
        return self.title


class ProjectScreenshot(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="screenshots")
    image = models.ImageField(upload_to="projects/screenshots/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]


class Review(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=120)   # private: shown only in the admin
    comment = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.name} ({'approved' if self.approved else 'pending'})"

class ContactMessage(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=120)
    message = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.name} ({self.created:%Y-%m-%d})"