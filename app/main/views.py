from flask import flash, render_template, redirect, url_for
from sqlalchemy import func
from .. import db
from ..models import User, Role, Teacher, Discipline, Student
from . import main
from .forms import NameForm, StudentForm
from datetime import datetime


@main.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@main.route('/alunos', methods=['GET', 'POST'])
def students_page():
    discipline_choices = {
        'dswa5': 'DSWA5',
        'gpsa5': 'GPSA5',
        'ihca5': 'IHCA5',
        'soda5': 'SODA5',
        'pjia5': 'PJIA5',
        'tcoa5': 'TCOA5',
    }

    student_registering_form = StudentForm()
    if student_registering_form.validate_on_submit():
        student_name = student_registering_form.studentName.data.strip()
        discipline_code = student_registering_form.discipline.data

        existing_student = Student.query.filter(
            func.lower(Student.student_name) == student_name.lower()
        ).first()

        if existing_student is not None:
            flash('Estudante já existe na base de dados!', 'warning')
            return redirect(url_for('.students_page'))

        discipline_obj = Discipline.query.filter_by(name=discipline_code).first()
        if discipline_obj is None:
            discipline_obj = Discipline(name=discipline_code)
            db.session.add(discipline_obj)
            db.session.commit()

        student = Student(
            student_name=student_name,
            discipline_id=discipline_obj.id
        )
        db.session.add(student)
        db.session.commit()

        flash('Aluno cadastrado com sucesso!', 'success')
        return redirect(url_for('.students_page'))

    students = Student.query.all()
    return render_template(
        'students_page.html',
        form=student_registering_form,
        students=students,
        discipline_choices=discipline_choices
    )