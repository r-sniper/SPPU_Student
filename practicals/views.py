import getpass  # To get username of the system
import os  # To update database for recursion visir every file in directory
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import StreamData, AllSubject, Assignment
from pygments import highlight
from pygments.lexers.c_cpp import CppLexer
from pygments.formatters.html import HtmlFormatter


# Homepage
def home(request):
    # .distinct()to only get single copies of all streams
    all_streams = StreamData.objects.values_list('stream', flat=True).distinct()
    return render(request, 'practicals/home.html', {
        'all_streams': all_streams,
    })


def test(request):
    if request.GET.get("Go") or request.GET.get("change"):
        stream = request.GET.get('stream')
        year = request.GET.get('year')
        stream_obj = StreamData.objects.get(stream=stream, year=year)
        base_directory = ''
        if getpass.getuser() == 'rsniper':
            base_directory = '/home/rsniper/SPPU_Student/'
        all_subjects = stream_obj.allsubject_set.all()
        assignments = all_subjects[0].assignment_set.all()
        default_assignment = assignments[0]
        filename = default_assignment.filename
        directory = base_directory + 'codes/' + stream + '/' + year + '/' + all_subjects[0].subject + '/' + filename
        fp = open(directory, 'r')
        code = fp.read().split('*/')  # To not display question while viewing code
        fp.close()
        test_code = highlight(code[1], CppLexer(), HtmlFormatter())
        # print(test_code)
        all_stream = StreamData.objects.values_list('stream', flat=True).distinct()
        all_year = StreamData.objects.filter(stream=stream).values_list('year', flat=True).distinct()
        print(all_stream)
        print(all_year)
        return render(request, 'practicals/subject.html', {
            'all_subjects': all_subjects,
            'assignment': default_assignment,
            'test_code': test_code,
            'all_stream': all_stream,
            'all_year': all_year,
            'selected_stream': stream,
            'selected_year': year
        })
    elif request.is_ajax():
        print("in ajax")
        data = (request.GET.get('select_assignment')).split(' ')
        print(data)

        assignment_id = data[1]
        base_directory = ''
        if getpass.getuser() == 'rsniper':
            base_directory = '/home/rsniper/SPPU_Student/'
        assignment = Assignment.objects.get(id=assignment_id)
        subject_obj = assignment.subject_obj
        stream_obj = subject_obj.stream_obj
        stream = stream_obj.stream
        year = stream_obj.year
        filename = assignment.filename
        directory = base_directory + 'codes/' + stream + '/' + year + '/' + subject_obj.subject + '/' + filename
        fp = open(directory, 'r')
        code = fp.read().split('*/')  # To not display question while viewing code
        fp.close()
        test_code = highlight(code[1], CppLexer(), HtmlFormatter())
        # print(test_code)
        print(data)
        return render(request, 'practicals/code.html', {
            'assignment': assignment,
            'test_code': test_code,
        })
    else:
        return HttpResponse("Some Error Occured. ")


#
#
# # This adds all the new codes to the database
# # Warning do not use on hosted server- only on local server.
def refresh(request):
    # Notice here 'rsniper' is just the username of the currently hosted site on pythonanywhere.
    # It is subjected to change
    if getpass.getuser() == 'rsniper':
        return HttpResponse("Please don't use this URL just yet")
    osdir = os.walk('codes/')
    added_streams = []
    added_subjects = []
    added_programs = []
    every_directory = set((), )
    for root, dirs, files in osdir:
        if root.count('/') == 3 and files:
            # print(root)
            # print(files)
            line = root.split('/')
            for f in files:
                temp = (line[1], line[2], line[3], f)
                every_directory.add(temp)

                # print('Stream:' + line[2])

    for s in every_directory:
        stream = s[0]
        year = s[1]
        subject = s[2]
        filename = s[3]
        title = filename.split('.')[1]
        # Important add base_directory to directory when deploying

        # base_directory = '/home/rsniper/SPPU_Student/'
        directory = 'codes/' + stream + '/' + year + '/' + subject + '/' + filename
        try:
            fp = open(directory, 'r')
        except IOError:
            return HttpResponse("File connot be opened")
        problem = fp.read().split("/*")[1].split("*/")[0]
        fp.close()

        if StreamData.objects.filter(stream=stream, year=year):
            print("Exists")
        else:
            new_stream = StreamData(stream=stream, year=year)
            new_stream.save()
            print("Dosent")
            added_streams.append(stream)

        if AllSubject.objects.filter(stream_obj=StreamData.objects.get(stream=stream, year=year),
                                     subject=subject):
            print("Exists")
        else:
            new_subject = AllSubject(stream_obj=StreamData.objects.get(stream=stream, year=year),
                                     subject=subject)
            new_subject.save()
            added_subjects.append(subject)

        if Assignment.objects.filter(subject_obj=AllSubject.objects.get(subject=subject,
                                                                        stream_obj=StreamData.objects.get(stream=stream,
                                                                                                          year=year)),
                                     filename=filename, title=title, problem_statement=problem):
            print("Exists")
        else:
            new_assignment = Assignment(subject_obj=AllSubject.objects.get(subject=subject,
                                                                           stream_obj=StreamData.objects.get(
                                                                               stream=stream,
                                                                               year=year)),
                                        filename=filename, title=title, problem_statement=problem)
            new_assignment.save()
            added_programs.append(new_assignment.title)
    return render(request, 'practicals/new_addition.html',
                  {
                      'stream_count': len(added_streams), 'subject_count': len(added_subjects),
                      'program_count': len(added_programs),
                      'streams': stream, 'subjects': added_subjects, 'programs': added_programs
                  })
