from django import forms
from .models import Lesson,Comment,Reply,Assignment,Submission

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('lesson_id','name','position','branch','semester','video','ppt','notes')

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('assignment_id','name','position','branch','semester','file',)
   
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('submission_id','name','ans_file',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {"body":"Comment:"}
        widgets = {
            'body':forms.Textarea(attrs={'class':'form-control','rows':4,'cols':10}),
        }
   
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('reply_body',)
        widgets = {
            'reply_body':forms.Textarea(attrs={'class':'form-control','rows':2,'cols':10}),
        }
    