import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import WorkerForm, OrderForm, ContractForm, SickLeaveForm
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
            new_order = WorkOrder(receipt_date=date.today(),
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

                pdf = FPDF()
                pdf.add_page()
                pdf.add_font('Hack', '', 'Hack-Regular.ttf', uni=True)
                pdf.set_font('Hack', size=12)
                pdf.cell(200, 50, txt='Приказ о предоставлении отпуска', ln=1, align='C')
                vacation_string = ('Предоставить сотруднику ' + str(Worker.objects.get(id_worker=new_vacation.id_worker))
                                   + ', работающему на должности '
                                   + str(JobTitle.objects.get(id_job_title=EmploymentContract.objects.get(id_worker=new_vacation.id_worker).id_job_title))
                                   + ' подразделения ' + str(StructuralSubdivision.objects.get(id_subdivision=EmploymentContract.objects.get(id_worker=new_vacation.id_worker).id_subdivision))
                                   + ' с ' + str(new_vacation.receipt_date) + ' по ' + str(new_vacation.expiration_date) +'.')


                pdf.multi_cell(200, 10, txt=vacation_string, align='L')


                # Сохраняем PDF на сервере
                pdf_path = 'orders/Vacation_' + str(
                    new_vacation.id_vacation) + '.pdf'  # путь, куда будет сохранен PDF
                pdf.output('./media/' + pdf_path)  # сохранение PDF файл

                # Добавляем путь к PDF файлу в базу данных
                vacation = Vacation.objects.get(
                    id_vacation=new_vacation.id_vacation)  # Получаем объект из базы данных, куда вы хотите добавить путь к файлу
                vacation.file = pdf_path
                vacation.save()


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

                try:
                    new_job = JobTitle.objects.get(name=form.cleaned_data.get('job_title'))
                except JobTitle.DoesNotExist:
                    new_job = JobTitle(name=form.cleaned_data.get('job_title'))
                    new_job.save()
                try:
                    new_subdivision = StructuralSubdivision.objects.get(
                        name=form.cleaned_data.get('subdivision'))
                except StructuralSubdivision.DoesNotExist:
                    new_subdivision = StructuralSubdivision(name=form.cleaned_data.get('subdivision'))
                    new_subdivision.save()

                try:
                    new_pow = PlaceOfWork.objects.get(name=form.cleaned_data.get('pow'), id_job_title=new_job,
                                                      id_subdivision=new_subdivision)
                except PlaceOfWork.DoesNotExist:
                    new_pow = PlaceOfWork(name=form.cleaned_data.get('pow'), id_job_title=new_job,
                                          id_subdivision=new_subdivision,
                                          reseipt_date=form.cleaned_data.get('receipt_date'))
                    new_pow.save()

                current_contract = EmploymentContract(receipt_date=date.today(),
                                              salary=form.cleaned_data.get('salary'),
                                              id_worker=new_worker,
                                              id_place_of_work=new_pow,
                                              id_subdivision=new_subdivision,
                                              id_job_title=new_job)
                current_contract.save()

                new_recruitment = Recruitment(recruitment_date=date.today(),
                                              id_contract=current_contract,
                                              id_worker=new_worker,
                                              id_job_title=new_job,
                                              id_subdivision=new_subdivision,
                                              id_place_of_work=new_pow,
                                              id_order=new_order,
                                              id_user=request.user.id_user)
                new_recruitment.save()

                pdf = FPDF()
                pdf.add_page()
                pdf.add_font('Hack', '', 'Hack-Regular.ttf', uni=True)
                pdf.set_font('Hack', size=12)
                pdf.cell(200, 50, txt='Приказ о приеме на работу', ln=1, align='C')
                recruitment_string = ('Принять на работу ' + str(new_worker)
                                      + ' в ' + str(new_subdivision) + ' на должность ' + str(new_job) + '.')

                pdf.multi_cell(200, 10, txt=recruitment_string, align='L')
                pdf.cell(200,15,txt='С окладом ' + str(current_contract.salary) + 'руб.' , align='L',ln=1)
                contract_string = ('Трудовой договор от ' + str(current_contract.receipt_date) + ' №' + str(current_contract.id_contract) + '.')
                pdf.multi_cell(200,25,txt=contract_string, align='L')
                # Сохраняем PDF на сервере
                pdf_path = 'orders/Recruitment_' + str(
                    new_recruitment.id_recruitment) + '.pdf'  # путь, куда будет сохранен PDF
                pdf.output('./media/' + pdf_path)  # сохранение PDF файл

                # Добавляем путь к PDF файлу в базу данных
                recruitment = Recruitment.objects.get(
                    id_recruitment=new_recruitment.id_recruitment)  # Получаем объект из базы данных, куда вы хотите добавить путь к файлу
                recruitment.file = pdf_path
                recruitment.save()


            elif form.cleaned_data.get('orderType') == '3': #Увольнение

                current_contract = EmploymentContract.objects.get(id_worker=form.cleaned_data.get('dismissalEmployee'))

                new_dismissal = Dismissal(reason=form.cleaned_data.get('reason'),
                                          dismissal_date=date.today(),
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
                pdf.cell(200,50, txt='Приказ об увольнении', ln=1, align='C')
                dismissal_string = ('Уволить ' + str(date.today()) + ' с должности ' + JobTitle.objects.get(id_job_title=new_dismissal.id_job_title).name + ' подразделения '
                                    + StructuralSubdivision.objects.get(id_subdivision=new_dismissal.id_subdivision).name + ' cотрудника '
                                    + str(Worker.objects.get(id_worker=new_dismissal.id_worker))
                                    + ' c согласия работника. Расторгнуть трудовой договор от ' + str(current_contract.receipt_date) + ' №'
                                    + str(current_contract.id_contract) + ', заключенный с сотрудником.')

                pdf.multi_cell(200,10, txt=dismissal_string, align='L')

                reason_string = ('Основание: ' + new_dismissal.reason + '.')
                pdf.multi_cell(200,20, txt=reason_string, align='L')

                # Сохраняем PDF на сервере
                pdf_path = 'orders/Dismissal_' + str(
                    new_dismissal.id_dismissal) + '.pdf'  # путь, куда будет сохранен PDF
                pdf.output('./media/' + pdf_path)  # сохранение PDF файл

                # Добавляем путь к PDF файлу в базу данных
                dismissal = Dismissal.objects.get(
                    id_dismissal=new_dismissal.id_dismissal)  # Получаем объект из базы данных, куда вы хотите добавить путь к файлу
                dismissal.file = pdf_path
                dismissal.save()


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

        all_recruitments = Recruitment.objects.all()
        all_vacations = Vacation.objects.all()
        all_dismissals = Dismissal.objects.all()

        # Определите начало и конец последнего месяца
        end_date = timezone.now() 
        start_date = end_date - timedelta(days=30)
        print(end_date)
        print(start_date)

        # Получите все записи за последний месяц
        dismissals_last_month = Dismissal.objects.filter(dismissal_date__range=[start_date, end_date])
        vacations_last_month = Vacation.objects.filter(receipt_date__range=[start_date, end_date])
        recruitments_last_month = Recruitment.objects.filter(recruitment_date__range=[start_date, end_date])

        data = {
            'form': form,
            'contractForm': contractForm,
            'all_recruitments': all_recruitments,
            'all_vacations': all_vacations,
            'all_dismissals': all_dismissals,
            'dismissals_last': dismissals_last_month,
            'recruitments_last': recruitments_last_month,
            'vacations_last': vacations_last_month,
        }
        return render(request, 'main/orders.html', data)

@login_required
def concrete_worker(request, id):
    worker = Worker.objects.get(id_worker=id)
    contract = EmploymentContract.objects.get(id_worker=worker.id_worker)
    job = JobTitle.objects.get(id_job_title=contract.id_job_title).name
    subdivision = StructuralSubdivision.objects.get(id_subdivision=contract.id_subdivision).name

    try:
        worker_vacations = Vacation.objects.all().filter(id_worker=worker)
    except Vacation.DoesNotExist:
        worker_vacations = None

    try:
        worker_recruitments = Recruitment.objects.all().filter(id_worker=worker)
    except Recruitment.DoesNotExist:
        worker_recruitments = None

    try:
        worker_dismissals = Dismissal.objects.all().filter(id_worker=worker)
    except Dismissal.DoesNotExist:
        worker_dismissals = None

    print(worker_dismissals)
    print(worker_recruitments)
    print(worker_vacations)

    data = {
        'worker': worker,
        'job': job,
        'subdivision': subdivision,
        'vacations': worker_vacations,
        'recruitments': worker_recruitments,
        'dismissals': worker_dismissals,
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

    if request.method == 'POST':
        form = SickLeaveForm(request.POST)
        if form.is_valid():
            new_sick = SickLeave(receipt_date=form.cleaned_data.get('startDate'),
                             expiration_date=form.cleaned_data.get('endDate'),
                             id_worker=AppUser.objects.get(id_user=id).id_worker)
            new_sick.save()

        return redirect('/')

    elif request.method == 'GET':
        form = SickLeaveForm()
        user = request.user
        user_data = Worker.objects.get(id_worker=user.id_worker)

        try:
            worker_vacations = Vacation.objects.all().filter(id_worker = user_data)
        except Vacation.DoesNotExist:
            worker_vacations = None

        try:
            worker_recruitments = Recruitment.objects.all().filter(id_worker = user_data)
        except Recruitment.DoesNotExist:
            worker_recruitments = None

        try:
            worker_dismissals = Dismissal.objects.all().filter(id_worker = user_data)
        except Dismissal.DoesNotExist:
            worker_dismissals = None

        try:
            contract = EmploymentContract.objects.get(id_worker=user.id_worker)
        except EmploymentContract.DoesNotExist:
            contract = None

        if contract is not None:
            job = JobTitle.objects.get(id_job_title=contract.id_job_title)
            subdivision = StructuralSubdivision.objects.get(id_subdivision=contract.id_subdivision)

            data = {
                'user_data': user_data,
                'job': job.name,
                'subdivision': subdivision.name,
                'vacations': worker_vacations,
                'recruitments': worker_recruitments,
                'dismissals': worker_dismissals,
                'form': form,
            }
        else:
            data = {
                'user_data': user_data,
                'vacations': worker_vacations,
                'recruitments': worker_recruitments,
                'dismissals': worker_dismissals,
                'form': form,
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