from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib import messages
from .forms import ActivityForm, LeadForm, NoteForm
from .models import Lead
from .ai_service import (
    AIServiceUnavailable,
    generate_follow_up,
    generate_lead_summary,
)
@login_required
def lead_list(request):
    leads = Lead.objects.all().order_by("-created_at")

    return render(
        request,
        "crm/lead_list.html",
        {"leads": leads},
    )
@login_required
def generate_summary(request, pk):
    lead = get_object_or_404(
        Lead,
        pk=pk,
    )

    if request.method == "POST":

        try:
            summary = generate_lead_summary(
                lead
            )

        except AIServiceUnavailable:
            messages.error(
                request,
                "AI is temporarily unavailable. "
                "Please try again shortly.",
            )

            return redirect(
                "lead_detail",
                pk=lead.pk,
            )

        lead.ai_summary = summary

        lead.save(
            update_fields=[
                "ai_summary",
                "updated_at",
            ]
        )

        messages.success(
            request,
            "AI summary generated successfully.",
        )

    return redirect(
        "lead_detail",
        pk=lead.pk,
    )
@login_required
def generate_ai_follow_up(request, pk):
    lead = get_object_or_404(
        Lead,
        pk=pk,
    )

    if request.method == "POST":

        try:
            follow_up = generate_follow_up(
                lead
            )

        except AIServiceUnavailable:
            messages.error(
                request,
                "AI is temporarily unavailable. "
                "Please try again shortly.",
            )

            return redirect(
                "lead_detail",
                pk=lead.pk,
            )

        lead.ai_follow_up = follow_up

        lead.save(
            update_fields=[
                "ai_follow_up",
                "updated_at",
            ]
        )

        messages.success(
            request,
            "Follow-up message generated successfully.",
        )

    return redirect(
        "lead_detail",
        pk=lead.pk,
    )@login_required
def dashboard(request):
    today = timezone.localdate()

    total_leads = Lead.objects.count()

    qualified_leads = Lead.objects.filter(
        status=Lead.Status.QUALIFIED
    ).count()

    won_leads = Lead.objects.filter(
        status=Lead.Status.WON
    ).count()

    overdue_followups = Lead.objects.filter(
        follow_up_date__lt=today
    ).exclude(
        status__in=[
            Lead.Status.WON,
            Lead.Status.LOST,
        ]
    ).count()

    if total_leads > 0:
        conversion_rate = round(
            (won_leads / total_leads) * 100,
            1,
        )
    else:
        conversion_rate = 0

    pipeline = (
        Lead.objects
        .values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )

    source_breakdown = (
        Lead.objects
        .values("source")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    upcoming_followups = (
        Lead.objects
        .filter(
            follow_up_date__gte=today,
        )
        .exclude(
            status__in=[
                Lead.Status.WON,
                Lead.Status.LOST,
            ]
        )
        .order_by("follow_up_date")[:5]
    )

    context = {
        "total_leads": total_leads,
        "qualified_leads": qualified_leads,
        "won_leads": won_leads,
        "overdue_followups": overdue_followups,
        "conversion_rate": conversion_rate,
        "pipeline": pipeline,
        "source_breakdown": source_breakdown,
        "upcoming_followups": upcoming_followups,
    }

    return render(
        request,
        "crm/dashboard.html",
        context,
    )

@login_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    notes = lead.notes.all().order_by("-created_at")
    activities = lead.activities.all().order_by("-created_at")

    note_form = NoteForm()
    activity_form = ActivityForm()

    return render(
        request,
        "crm/lead_detail.html",
        {
            "lead": lead,
            "notes": notes,
            "activities": activities,
            "note_form": note_form,
            "activity_form": activity_form,
        },
    )
@login_required
def lead_create(request):
    if request.method == "POST":
        form = LeadForm(request.POST)

        if form.is_valid():
            lead = form.save()
            return redirect("lead_detail", pk=lead.pk)

    else:
        form = LeadForm()

    return render(
        request,
        "crm/lead_form.html",
        {
            "form": form,
            "title": "Create Lead",
        },
    )

@login_required
def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":
        form = LeadForm(
            request.POST,
            instance=lead,
        )

        if form.is_valid():
            lead = form.save()
            return redirect("lead_detail", pk=lead.pk)

    else:
        form = LeadForm(instance=lead)

    return render(
        request,
        "crm/lead_form.html",
        {
            "form": form,
            "title": "Edit Lead",
        },
    )
@login_required
def note_create(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)

            note.lead = lead
            note.author = request.user

            note.save()

    return redirect("lead_detail", pk=lead.pk)


@login_required
def activity_create(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":
        form = ActivityForm(request.POST)

        if form.is_valid():
            activity = form.save(commit=False)

            activity.lead = lead

            activity.save()

    return redirect("lead_detail", pk=lead.pk)
@login_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":
        lead.delete()
        return redirect("lead_list")

    return render(
        request,
        "crm/lead_confirm_delete.html",
        {"lead": lead},
    )