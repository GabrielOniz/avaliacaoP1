from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class Discipline(db.Model):
    __tablename__ = 'disciplines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    teachers = db.relationship('Teacher', back_populates='discipline')
    students = db.relationship('Student', back_populates='discipline')

    def __repr__(self):
        return '<Discipline %r>' % self.name


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(64), index=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'))
    discipline = db.relationship('Discipline', back_populates='students')

    def __repr__(self):
        return '<Student %r>' % self.student_name


class Teacher(db.Model):

    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(64), unique=True, index=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'))
    discipline = db.relationship('Discipline', back_populates='teachers')

    def __repr__(self):
        return '<Teacher %r>' % self.teacher_name