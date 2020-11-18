import hashlib
from cryptography.fernet import Fernet
from datetime import datetime
from aifc import Error

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from course.models import Course, Module, Enrollment, Coupon,Subject
from account.models import TeacherProfile,StudentProfile
from django.db.models import Q
from course.api.serializer import (CourseSerializer,
                                   CourseDetailSerializer,
                                   CourseCreateSerializer,
                                   ModuleSerializer,
                                   CourseEnrollSerializer,
                                   EnrolledCourseSerializer,
                                   MycoursesSerializer,
                                   CouponSerializer,
                                   SubjectSerializer)
from rest_framework.generics import( ListAPIView,
                                     RetrieveAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateAPIView,
                                     UpdateAPIView,
                                     ListCreateAPIView)
from rest_framework.permissions import IsAuthenticated

# Views for Unauthenticated Users

# List all Courses

class ListCourse(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# course info

class CourseRetrieve(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer


# views for authenticated users

# creating courses and modules
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def CreateCourse(request,pk):
    teacher = TeacherProfile.objects.get(user=request.user)
    subject = Subject.objects.get(id=pk)
    course = Course(author=teacher,subject=subject)
    serializer = CourseCreateSerializer(course,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

# class CreateCourseView(CreateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseCreateSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         print("user:-" ,self.request.user)
#         teacher = TeacherProfile.objects.get(user=self.request.user.id)
#         subject = Subject.objects.get(id)
#         serializer.save(author=teacher)

# updating courses and modules within the course
class UpdateCourse(RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated]


# delete course

@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def DeleteCourse(request,pk):
    course=Course.objects.get(id=pk)
    course.delete()
    return Response("Course Successfully Deleted")


# get list of courses related to the teacher
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def TeacherCourses(request):
    teacher = TeacherProfile.objects.get(user=request.user)
    courses = Course.objects.filter(author=teacher)
    serializer = CourseDetailSerializer(courses,many=True)
    return Response(serializer.data)

# creating a separate module


@permission_classes((IsAuthenticated))
@api_view(['POST'])
def CreateModule(request,pk):
    course = Course.objects.get(id=pk)
    module = Module(course=course)
    print("important", module.course)
    if request.method == "POST":
        serializer = ModuleSerializer(module, data=request.data)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors)

# update Module

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def UpdateModule(request,pk):
    module=Module.objects.get(id=pk)
    serializer = ModuleSerializer(instance=module,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# Delete Module

@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def DeleteModule(request,pk):
    module=Module.objects.get(id=pk)
    module.delete()
    return Response({"message":"Module Successfully Deleted"})


# views for Students

# course Enroll

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def EnrollCourse(request,pk):
    course = Course.objects.get(id=pk)
    student = StudentProfile.objects.get(user=request.user)
    couponList = Coupon.objects.filter(course=course)
    for c in couponList:
        coupon = str(c.id)+":"+str(c.course.id)+":"+str(c.expire_date)
        couponHash = hashlib.shake_256(coupon.encode()).hexdigest(5)
        if str(request.data['coupon_key'])==str(couponHash):
            enroll = Enrollment(course=course,student=student, enroll_key=request.data['coupon_key'])
            condition = c.isValid==True and c.isIssued==True
            if request.method == "POST":
                if condition:
                    e = Enrollment.objects.filter(course=course, student=student).first()
                    if not e:
                        serializer = CourseEnrollSerializer(enroll, data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            couponSerializer = CouponSerializer(instance=c, data=request.data)
                            if couponSerializer.is_valid():
                                couponSerializer.save(isValid=False)
                                serializer.data['student']['user'].pop('password')
                            return Response(serializer.data)
                        return Response(serializer.errors)
                    return Response("You have already enrolled this course...")
                return Response("Coupon is not valid")

    return Response("coupon is not found")



# Listing Enrolled Courses
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def MyCourses(request):
    student = StudentProfile.objects.get(user=request.user)
    courses_enrolled = Enrollment.objects.filter(student=student)
    serializer = MycoursesSerializer(courses_enrolled,many=True)
    return Response(serializer.data)



# accessing enrolled courses
class ViewEnrolledCourse(RetrieveAPIView):
    serializer_class = (EnrolledCourseSerializer)
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]



@api_view(['POST'])
def CouponGenerator(request, count, pk):
    course = Course.objects.filter(id=pk).first()
    expire_date = datetime(2021, 11, 7)

    try:
        couponList = Coupon.objects.bulk_create(
            [
                Coupon(course=course, expire_date=expire_date, coupon_key="")
                for __ in range(count)
            ]
        )
        couponL = Coupon.objects.filter(coupon_key="")
        for c in list(couponL):
            serializer = CouponSerializer(instance=c, data=request.data)
            if serializer.is_valid():
                coupon = str(c.id) + ":" + str(c.course.id) + ":" + str(c.expire_date)
                coupon_key = hashlib.shake_256(coupon.encode()).hexdigest(5)
                serializer.save(coupon_key=coupon_key)
        return Response({"message":"successfully created"})
    except Error:
        return  Response({"message":"Unable to create the bulk of coupons"})
    else:
        return Response({"message":"Something went wrong"})

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def AvailableCoupon(request, pk):
    course = Course.objects.get(id=pk)
    couponList = Coupon.objects.filter(isValid=True, course=course )
    for i in range(len(couponList)):
        coupon = str(couponList[i].id)+":"+str(couponList[i].course.id)+":"+str(couponList[i].expire_date)
        couponList[i].coupon_key = hashlib.shake_256(coupon.encode()).hexdigest(5)

    serializer = CouponSerializer(couponList, many=True)
    return Response(serializer.data)

# issue coupons

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def IssueCoupon(request):
    for i in range(len(request.data['issued_coupons'])):
        coupon = Coupon.objects.get(id=request.data['issued_coupons'][i])
        serializer = CouponSerializer(instance=coupon,data=request.data)
        if serializer.is_valid():
            serializer.save(isIssued=True)
    return Response({"message":"successfully issued"})

# create subject
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def CreateSubject(request):
    author = TeacherProfile.objects.get(user=request.user)
    serializer = SubjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=author)
    return Response(serializer.data)

# update subject

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def UpdateSubject(request,pk):
    subject = Subject.objects.get(id=pk)
    serializer = SubjectSerializer(instance=subject, data=request.data)
    if serializer.is_valid():
        serializer.save()
        print("updated")
    return Response(serializer.data)

# delete subject

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def DeleteSubject(request,pk):
    subject = Subject.objects.get(id=pk)
    subject.delete()
    return Response("Subject Successfully Deleted")

# subject list
@api_view(['GET'])
def SubjectList(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)

# subject list of teacher

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def TeacherSubject(request):
    teacher = TeacherProfile.objects.get(user=request.user)
    subject = Subject.objects.filter(author=teacher)
    serializer = SubjectSerializer(subject,many=True)
    return Response(serializer.data)





