
create database polytech_attendance;

-- Table `users`.
create table polytech_attendance.users (
	user_id int not null auto_increment,
    user_login varchar(255) not null,
    user_password varchar(255) not null,
    
    constraint UC_users_login unique (user_login),
    primary key(user_id)
);

-- Table `groupleaders`.
create table polytech_attendance.groupleaders (
	groupleader_id int not null auto_increment,
    user_id int not null,
    groupleader_name varchar(255) not null,
    
    constraint FK_groupleader_user foreign key (user_id) references polytech_attendance.users(user_id),
    primary key(groupleader_id)
);

-- Table `teachers`.
create table polytech_attendance.teachers (
	teacher_id int not null auto_increment,
    user_id int not null,
    teacher_name varchar(255) not null,
    
    constraint FK_teacher_user foreign key (user_id) references polytech_attendance.users(user_id),
    primary key(teacher_id)
);

-- Table `groups`.
create table polytech_attendance.groups (
	group_id int not null auto_increment,
    groupleader_id int not null,
    group_name varchar(255) not null,
    
    constraint UC_group_name unique (group_name),
    constraint FK_group_groupleader foreign key (groupleader_id) references polytech_attendance.groupleaders(groupleader_id),
    primary key (group_id)
);

-- Table `students`.
create table polytech_attendance.students (
	student_id int not null auto_increment,
    group_id int not null,
    student_name varchar(255) not null,
    student_is_foreign boolean not null,

    constraint FK_student_group foreign key (group_id) references polytech_attendance.groups (group_id),
    primary key (student_id)
);

-- Table `subject`.
create table polytech_attendance.subject (
	subject_id int not null auto_increment,
    group_id int not null,
    teacher_id int not null,
    subject_name varchar(255) not null,
    
    constraint UC_subject_name unique (subject_name),
    constraint FK_subject_group foreign key (group_id) references polytech_attendance.groups (group_id),
    constraint FK_subject_teacher foreign key (teacher_id) references polytech_attendance.teachers (teacher_id),
    primary key (subject_id)
);

-- Table `classes`.
create table polytech_attendance.classes (
	class_id int not null auto_increment,
    subject_id int not null,
    class_start_time time not null,
    class_end_time time not null,
    
    constraint FK_classes_subject foreign key (subject_id) references polytech_attendance.subject (subject_id),
    primary key (class_id)
);

-- Table `attendances`.
create table polytech_attendance.attendances (
	attendance_id int not null auto_increment,
    class_id int not null,
    student_id int not null,
    attendance_is_attendance boolean not null,
    
    constraint FK_attendances_class foreign key (class_id) references polytech_attendance.classes (class_id),
    constraint FK_attendances_student foreign key (student_id) references polytech_attendance.students (student_id),
    primary key (attendance_id)
);