from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import WorkerForm, OrderForm, ContractForm
from .models import *
from datetime import date, timedelta
from django.utils import timezone
from fpdf import FPDF, fpdf

fpdf.SYSTEM_TTFONTS = 'C:\Windows\Fonts'

def index(request):
    sick_leaves = SickLeave.objects.all().filter(expiration_date__gte=date.today())
    vacations = Vacation.objects.all().filter(expiration_date__gte=date.today())
    workers = Worker.objects.all()
    candidates = Candidate.objects.all()

    # вычисляем дату, равную 3 месяца назад
    three_months_ago = timezone.now() - timedelta(days=3 * 30)

    new_workers = EmploymentContract.objects.all().filter(receipt_date__gte=three_months_ago)
    dismissals = Dismissal.objects.all().filter(dismissal_date__gte=three_months_ago)
    new_candidates = Candidate.objects.all()




    data = {
        'sick_counter': len(sick_leaves),
        'vac_counter': len(vacations),
        'worker_counter': len(workers),
        'candidate_counter': len(candidates),
        'new_workers': len(new_workers),
        'dismissals': len(dismissals),
        'new_candidates': len(new_candidates),
    }
    return render(request, 'main/index.html', data)


@login_required
def candidates(request):
    list_candidates = []
    candidates = Candidate.objects.all()

    for candidate in candidates:
        resume = JobResume.objects.get(id_job_resume=candidate.id_job_resume)
        job = resume.position
        fio = resume.surname + ' ' + resume.name + ' ' + resume.patronymic



        list_candidates.append({'fio': fio,
                                'job': job,
                                'id': candidate.id_candidate
                                })

    data = {
        'candidates': list_candidates,
    }


    return render(request, 'main/candidates.html', data)

@login_required
def workers(request):
    list_workers = []
    
    workers = Worker.objects.all()

    for worker in workers:
        try:
            contract = EmploymentContract.objects.get(id_worker=worker.id_worker)
        except EmploymentContract.DoesNotExist:
            continue
        status = ''

        place = PlaceOfWork.objects.get(id_place_of_work=contract.id_place_of_work)

        job_title = JobTitle.objects.get(id_job_title=place.id_job_title)

        fio = worker.surname + ' ' + worker.name + ' ' + worker.patronymic
        vac = Vacation.objects.all().filter(expiration_date__gte=date.today(), id_worker=worker.id_worker)
        sick = SickLeave.objects.all().filter(expiration_date__gte=date.today(), id_worker=worker.id_worker)
        if len(vac) != 0:
            status = 'В отпуске'
        elif len(sick) != 0:
            status = 'На больничном'
        else:
            status = 'Активен'

        list_workers.append({'fio': fio,
                            'job': job_title.name,
                             'status': status,
                             'id': worker.id_worker,
                             })

    data = {
        'workers': list_workers,
    }


    return render(request, 'main/workers.html', data)

@login_required
def orders(request):
    if request.method == 'POST' and 'addOrder' in request.POST:
        form = OrderForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            new_order = WorkOrder(receipt_date=timezone.now(),
                                  order_number=form.cleaned_data.get('orderNumber'),
                                  id_user=request.user)
            new_order.save()
            if form.cleaned_data.get('orderType') == '1': #Отпуск
                new_vacation = Vacation(receipt_date=form.cleaned_data.get('startDate'),
                                        expiration_date=form.cleaned_data.get('endDate'),
                                        id_vacationtype=VacationType.objects.get(
                                        id_vacation_type=int(form.cleaned_data.get('orderType'))),
                                        id_worker=form.cleaned_data.get('employee'),
                                        id_order=new_order,
                                        id_user=request.user.id_user)
                new_vacation.save()
            elif form.cleaned_data.get('orderType') == '2': #Прием
                current_resume = JobResume.objects.get(id_job_resume=form.cleaned_data.get('candidate'))

                new_worker = Worker(surname=current_resume.surname,
                                    name=current_resume.name,
                                    patronymic=current_resume.patronymic,
                                    gender=current_resume.gender,
                                    adress=current_resume.adress,
                                    work_experience=current_resume.work_experience,
                                    birthday=current_resume.birthday,
                                    phone_number=current_resume.phone_number,
                                    photo=current_resume.photo)
                new_worker.save()

                current_candidate = Candidate.objects.get(id_job_resume=current_resume)

                current_user = AppUser.objects.get(id_candidate=current_candidate)
                current_user.id_candidate = None
                current_user.id_worker = new_worker
                current_user.role = 2
                current_user.save()

                current_candidate.delete()

                current_resume.delete()


            elif form.cleaned_data.get('orderType') == '3': #Увольнение

                current_contract = EmploymentContract.objects.get(id_worker=form.cleaned_data.get('dismissalEmployee'))

                new_dismissal = Dismissal(reason=form.cleaned_data.get('reason'),
                                          dismissal_date=timezone.now(),
                                          id_worker=form.cleaned_data.get('dismissalEmployee'),
                                          id_contract=current_contract,
                                          id_order=new_order,
                                          id_user=request.user.id_user,
                                          id_place_of_work=current_contract.id_place_of_work,
                                          id_job_title=current_contract.id_job_title,
                                          id_subdivision=current_contract.id_subdivision)
                new_dismissal.save()

                pdf = FPDF()
                pdf.add_page()
                pdf.add_font('Hack', '', 'Hack-Regular.ttf', uni=True)
                pdf.set_font('Hack', size=12)
                pdf.cell(200,10, txt='Приказ на увольнение', ln=1, align='C')

                pdf.output('./media/orders/Dismissal_' + str(new_dismissal.id_dismissal) + '.pdf')


            return redirect('/orders/')

    elif request.method == 'POST' and 'addContract' in request.POST:
        contractForm = ContractForm(request.POST)
        if contractForm.is_valid():
            print(contractForm.cleaned_data)

            try:
                new_job = JobTitle.objects.get(name=contractForm.cleaned_data.get('job_title'))
            except JobTitle.DoesNotExist:
                new_job = JobTitle(name=contractForm.cleaned_data.get('job_title'))
                new_job.save()
            try:
                new_subdivision = StructuralSubdivision.objects.get(name=contractForm.cleaned_data.get('subdivision'))
            except StructuralSubdivision.DoesNotExist:
                new_subdivision = StructuralSubdivision(name=contractForm.cleaned_data.get('subdivision'))
                new_subdivision.save()

            try:
                new_pow = PlaceOfWork.objects.get(name=contractForm.cleaned_data.get('pow'), id_job_title=new_job, id_subdivision=new_subdivision)
            except PlaceOfWork.DoesNotExist:
                new_pow = PlaceOfWork(name=contractForm.cleaned_data.get('pow'), id_job_title=new_job, id_subdivision=new_subdivision,reseipt_date=contractForm.cleaned_data.get('receipt_date'))
                new_pow.save()


            new_contract = EmploymentContract(receipt_date=contractForm.cleaned_data.get('receipt_date'),
                                              salary=contractForm.cleaned_data.get('salary'),
                                              id_worker=contractForm.cleaned_data.get('worker'),
                                              id_place_of_work=new_pow,
                                              id_subdivision=new_subdivision,
                                              id_job_title=new_job)
            new_contract.save()

        return redirect('/orders/')

    elif request.method == 'GET':
        form = OrderForm()
        contractForm = ContractForm()
        data = {
            'form': form,
            'contractForm': contractForm,
        }
        return render(request, 'main/orders.html', data)

@login_required
def concrete_worker(request, id):
    worker = Worker.objects.get(id_worker=id)
    contract = EmploymentContract.objects.get(id_worker=worker.id_worker)
    job = JobTitle.objects.get(id_job_title=contract.id_job_title).name
    subdivision = StructuralSubdivision.objects.get(id_subdivision=contract.id_subdivision).name

    data = {
        'worker': worker,
        'job': job,
        'subdivision': subdivision,
    }

    return render(request, 'main/concrete_worker.html', data)

@login_required
def concrete_candidate(request, id):
    candidate = Candidate.objects.get(id_candidate=id)
    resume = candidate.id_job_resume

    data = {
        'candidate': candidate,
        'resume': resume,
    }

    return render(request, 'main/concrete_candidate.html', data)

@login_required
def edit_worker(request,id):
    error = ''
    if request.method == 'POST':
        instance = get_object_or_404(Worker, id_worker=id)
        form_post = WorkerForm(request.POST or None, request.FILES, instance=instance)

        if form_post.is_valid():
            form_post.save()
            return redirect('/')
        else:
            error = 'Форма заполнена неверными данными!'
            data = {'form': form_post,
                    'error': error
                    }
            print(form_post.errors)
            return render(request, 'main/edit_worker.html', data)
    elif request.method == 'GET':
        worker = Worker.objects.get(id_worker=id)
        form = WorkerForm(instance=worker)


        data = {
            'form': form,
            'error': error
        }
        return render(request, 'main/edit_worker.html', data)


@login_required
def profile(request, id):
    user = request.user

    user_data = Worker.objects.get(id_worker=user.id_worker)
    try:
        contract = EmploymentContract.objects.get(id_worker=user.id_worker)
    except EmploymentContract.DoesNotExist:
        contact = None

    if contact is not None:
        job = JobTitle.objects.get(id_job_title=contract.id_job_title)
        subdivision = StructuralSubdivision.objects.get(id_subdivision=contract.id_subdivision)

        data = {
            'user_data': user_data,
            'job': job.name,
            'subdivision': subdivision.name,
        }
    else:
        data = {
            'user_data': user_data,
        }


    return render(request,'main/worker_page.html', data)


@login_required
def candidate_page(request, id):
    user = request.user

    candidate = Candidate.objects.get(id_candidate=user.id_candidate)
    user_data = JobResume.objects.get(id_job_resume=candidate.id_job_resume)
    edu = Candidateeducation.objects.all().filter(id_candidate=user.id_candidate)

    edu_data = []

    for e in edu:
        edu_data.append(EducationalData.objects.get(id_educational_data=e.id_educational_data))


    data = {
        'user_data': user_data,
        'educations': edu_data,
    }

    return render(request,'main/candidate_page.html', data)