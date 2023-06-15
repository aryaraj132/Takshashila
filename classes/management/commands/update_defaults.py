from django.core.management.base import BaseCommand
from classes.models import Branch,Semester,Subject,Lesson,Assignment,Submission
BRANCES = {
    "CSE": "Computer Science and Engineering",
    "ECE": "Electronics and Communication Engineering",
    "EE": "Electrical Engineering",
    "ME": "Mechanical Engineering",
    "CE": "Civil Engineering",
}
SEMESTERS = {
    "sem-1" : "semester 1",
    "sem-2" : "semester 2",
    "sem-3" : "semester 3",
    "sem-4" : "semester 4",
    "sem-5" : "semester 5",
    "sem-6" : "semester 6",
    "sem-7" : "semester 7",
    "sem-8" : "semester 8",
}

class Command(BaseCommand):
    help = "Populate Semester and Branches"

    def handle(self, *args, **options):
        # for branch in BRANCES:
        #     branch_obj = Branch.objects.get(slug=branch, name=BRANCES[branch])
        #     for sem in SEMESTERS:
        #         sem_obj = Semester.objects.get(slug=sem, name=SEMESTERS[sem], branch=branch_obj)
        #         sem_obj.slug = sem+"_"+branch
        #         sem_obj.save()
        # print("Done populating Branches and Semesters")
        Lesson.objects.all().delete()