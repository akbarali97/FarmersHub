from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.db import connection
from django.contrib import messages
from pfapp.models import Person, User_locations, user_details, products, contracts, contract_orders, reviews
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
import uuid
import json
import datetime

def rfact (cr,r):
    return {i[1][0]: r[i[0]] for i in enumerate(cr.description)}

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def checkuser(request):
    user_l = ""
    if request.session.has_key('usr'):
        user_l = request.session['usr']
    return user_l


def index(request):
        signup_page = ''
        if 'signin' in request.POST:
            login(request)
        if checkuser(request):
            loged_user = request.session['usr']
            if loged_user.get('type') == 'consumer':
                return redirect('Explore/')
            else:
                return redirect('Profile/')
        else:
            # create_kit(2,3,'[5,4,3,2]','1860')
            return render(request, 'index.html', {'usr': checkuser(request), 'signup_page': signup_page})
        
# to view the farmers profile page
def view_profile(request,email):
    if checkuser(request):
        user_exist = 0
        content_view = 'Explore_Farmers'
        with connection.cursor() as c:
            c.execute("""SELECT * FROM pfapp_person 
            JOIN pfapp_user_locations ON pfapp_user_locations.person_id = pfapp_person.id 
            JOIN pfapp_user_details ON pfapp_user_details.person_id = pfapp_person.id 
            WHERE pfapp_person.email=%s LIMIT 1""", [email])
            c.cursor.row_factory = rfact
            q_usr = c.fetchone()
        user_exist = 1
        p = Person.objects.get(email=email)
        p = p.id
        c = contracts.objects.filter(Person__id=p)
        review_ratings = reviews.objects.filter(reviewee_id=p)
        return render(request, 'dashboard_index.html', {'usr': checkuser(request), 'content_view': content_view,'qusr':q_usr,'user_exist':user_exist,'c':c,'review_ratings':review_ratings})
    else:
        messages.info(request, 'Login Now to view this page!!!')
        return redirect('/')

# when buy button clicked from contracts tab on farmer's profile page.
def checkout(request):
    if request.is_ajax and request.method == "POST":
        data = json.loads(request.POST.get('data'))
        consumer_id = data.get('consumerid')
        farmer_id = data.get('farmerid')
        contract_ids = data.get('listofids')
        # contract_ids_str = str(contract_ids)
        # total = data.get('total')
        orderstatus = 'pending'
        datetime = json.dumps(datetime_dict())
        for i in range(0,len(contract_ids)):
            with connection.cursor() as c:
                c.execute("""INSERT INTO pfapp_contract_orders 
                (seller_id,buyer_id,contract_id,order_datetime,order_status) 
                VALUES(%s,%s,%s,%s,%s)""", [farmer_id,consumer_id,contract_ids[i],datetime,orderstatus])
        # create_kit(consumer_id,farmer_id,contract_ids_str,total)
        return HttpResponse('success')

def datetime_dict():
    x = datetime.datetime.now()
    x = str(x)
    date = x[0:10]
    time = x[11:16]
    dic = {'date':date,'time':time}
    return dic

# view after cart button 'buynow' is clicked for consumer
def orders(request):
    if checkuser(request):
        content_view = 'orders'
        consumer = request.session['usr'].get('id')
        with connection.cursor() as c:
            c.execute("SELECT * FROM pfapp_contract_orders JOIN pfapp_person ON pfapp_person.id=pfapp_contract_orders.seller_id JOIN pfapp_contracts ON pfapp_contracts.id=pfapp_contract_orders.contract_id JOIN pfapp_user_details ON pfapp_user_details.person_id=pfapp_person.id WHERE pfapp_contract_orders.buyer_id=%s ",[consumer])
            k = dictfetchall(c)
            # print(k)
        return render(request, 'dashboard_index.html' ,{'usr': checkuser(request),'content_view':content_view,'orders':k})
    else:
        messages.info(request, 'Login Now to view this page!!')
        return redirect('/')

def orderstatus(request,order_id,status):
    if checkuser(request):
        if (status == 'cancelled'):
            if (request.session['usr'].get('type') == 'consumer'):    
                c = contract_orders.objects.get(order_id=order_id)
                c.order_status = status
                c.save()
                return redirect('/orders/')
            else:
                messages.info(request, "You Can't perform this operation")
                return redirect('/')
        elif status=='accepted' or status=='declined':
            if (request.session['usr'].get('type') == 'farmer'):    
                c = contract_orders.objects.get(order_id=order_id)
                c.order_status = status
                c.save()
                return redirect('/Contracts_Manager/New_Request/')
            else:
                messages.info(request, "You Can't perform this operation")
                return redirect('/')
        else:
            messages.info(request, "Unkown Request")
            return redirect('/')
    else:
        messages.info(request, 'Login Now to view this page!!')
        return redirect('/')


# To view farmers near the registered location of the consumer
def Explore(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        user_exist = 0
        content_view = 'Explore_Farmers'
        location = request.session['usr'].get('locality')
        with connection.cursor() as c:
            c.execute(f"SELECT * FROM pfapp_person JOIN pfapp_user_locations ON pfapp_user_locations.person_id = pfapp_person.id JOIN pfapp_user_details ON pfapp_user_details.person_id = pfapp_person.id WHERE pfapp_person.type='farmer' AND pfapp_user_locations.locality='{location}' ")
            farmer = dictfetchall(c)
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view,'farmers':farmer,'user_exist':user_exist}, request))
    else:
        messages.info(request, 'Login Now to view this page!!')
        return redirect('/')

def Settings(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Settings'
        if 'settings_pwd_button' in request.POST:
            # password updation code here
            messages.info(request, 'Password Updated sucessfully!')
        if 'settings_location_button' in request.POST:
            # location updation code here
            messages.info(request, 'Location Updated sucessfully!')
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!!')
        return redirect('/')


def Delivery_Conformation(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Delivery_Conformation'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!!')
        return redirect('/')

def My_Earnings(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'My_Earnings'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!!')
        return redirect('/')

def Learn_Farming(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Learn_Farming'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def Surpluse_Market(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Surpluse_Market'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def My_Farmers(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'My_Farmers'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def My_Customers(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'My_Customers'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def Dispatch_Manager(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Dispatch_Manager'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def Customer_Reviews(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Customer_Reviews'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def addreview(request):
    if checkuser(request):
        if 'reviewbtn' in request.POST:
            reviewer = request.session['usr'].get('id')
            reviewee = request.POST['reviewee']
            review = request.POST['reviewtext']
            rating = request.POST['star']
            # print(reviewer,reviewee,review,rating,sep='\n')
            with connection.cursor() as c:
                c.execute(""" INSERT INTO pfapp_reviews
                            (reviewer_id,reviewee_id,review,rating)
                             VALUES(%s,%s,%s,%s) """,[reviewer,reviewee,review,rating])
            # reviews.objects.create(reviewee=reviewee,reviewer=reviewer,review=review,rating=rating)
            r = reviews.objects.filter(reviewee=reviewee).count()
            print(r)
            email = Person.objects.get(id=reviewee).email
            return redirect(f'/user/{email}/')
    else:
        messages.info(request, 'Login Now to view this page!!')
        return redirect('/')



def New_Request(request):
    if checkuser(request):
        content_view = 'Contracts_Manager'
        content_view_sub = 'New_Request'
        farmer = request.session['usr'].get('id')
        with connection.cursor() as c:
            c.execute("SELECT * FROM pfapp_contract_orders JOIN pfapp_person ON pfapp_person.id=pfapp_contract_orders.buyer_id JOIN pfapp_contracts ON pfapp_contracts.id=pfapp_contract_orders.contract_id JOIN pfapp_user_details ON pfapp_user_details.person_id=pfapp_person.id WHERE pfapp_contract_orders.seller_id=%s AND pfapp_contract_orders.order_status='pending'",[farmer])
            k = dictfetchall(c)
        return render(request, 'dashboard_index.html' ,{'usr': checkuser(request),'content_view':content_view,'orders':k,'content_view_sub':content_view_sub})
    else:
        messages.info(request, 'Login Now to view this page!!')
        return redirect('/')

def Active_Contracts(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Contracts_Manager'
        content_view_sub = 'Active_Contracts'
        person = request.session['usr']
        person = person.get('id')
        c = contracts.objects.filter(Person__id=person)
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view,'content_view_sub': content_view_sub,'c':c}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def Active_Orders(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        farmer = request.session['usr'].get('id')
        content_view = 'Contracts_Manager'
        content_view_sub = 'Active_Orders'
        with connection.cursor() as c:
            c.execute("SELECT * FROM pfapp_contract_orders JOIN pfapp_person ON pfapp_person.id=pfapp_contract_orders.buyer_id JOIN pfapp_contracts ON pfapp_contracts.id=pfapp_contract_orders.contract_id JOIN pfapp_user_details ON pfapp_user_details.person_id=pfapp_person.id WHERE pfapp_contract_orders.seller_id=%s AND pfapp_contract_orders.order_status='accepted'",[farmer])
            k = dictfetchall(c)
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view,'content_view_sub': content_view_sub,'orders':k}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def Add_Contracts(request):
    if checkuser(request):
        if 'create' in request.POST:
            person = request.session['usr']
            person = person.get('id')
            product = request.POST['product_name']
            product = products.objects.get(name=product)
            product = product.id
            duration = request.POST['duration']
            frequency = request.POST['frequency']
            quantity = request.POST['quantity']
            price = request.POST['price']
            duration_unit = request.POST['duration_unit']
            frequency_unit = request.POST['frequency_unit']
            quantity_unit = request.POST['quantity_unit']
            price_unit = request.POST['price_unit']
            status = 'availabe'
            with connection.cursor() as c:
                c.execute("INSERT INTO pfapp_contracts (Person_id,product_id,quantity,quantity_unit,duration,duration_unit,frequency,frequency_unit,price,price_unit,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [person,product,quantity,quantity_unit,duration,duration_unit,frequency,frequency_unit,price,price_unit,status])
            messages.info(request, 'Contract successfully created')
            return redirect('/Contracts_Manager/Active_Contracts/')
        else:
            content_view = 'Contracts_Manager'
            content_view_sub = 'Add_Contracts'
            p = products.objects.all()
            return render(request, 'dashboard_index.html', {'usr': checkuser(request), 'content_view': content_view,'content_view_sub': content_view_sub,'p':p})
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def Profile(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Profile'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')


def My_Contracts(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'My_Contracts'
        consumer = request.session['usr'].get('id')
        with connection.cursor() as c:
            c.execute("""SELECT * FROM pfapp_contract_orders 
            JOIN pfapp_person ON pfapp_person.id=pfapp_contract_orders.seller_id 
            JOIN pfapp_contracts ON pfapp_contracts.id=pfapp_contract_orders.contract_id 
            JOIN pfapp_user_details ON pfapp_user_details.person_id=pfapp_person.id 
            WHERE pfapp_contract_orders.buyer_id=%s AND pfapp_contract_orders.order_status='accepted'""",[consumer])
            k = dictfetchall(c)
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view,'orders':k}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')



def login(request):
    if request.method == "POST":
        email = request.POST['email']
        pwd = request.POST['pwd']
        # # sql = f"SELECT * FROM pfapp_person WHERE email='{email}' AND pwd='{pwd}' LIMIT 1"
        # sql = f"SELECT * FROM pfapp_person, pfapp_user_details, pfapp_user_locations WHERE pfapp_person.email ='{email}' AND pwd='{pwd}' LIMIT 1"
        # # database connection
        # c = connection.cursor()
        # c.execute(sql)
        # c.cursor.row_factory = rfact
        # user = c.fetchone()
        # c.close()

        with connection.cursor() as c:
            c.execute(f"SELECT * FROM pfapp_person JOIN pfapp_user_locations ON pfapp_user_locations.person_id = pfapp_person.id JOIN pfapp_user_details ON pfapp_user_details.person_id = pfapp_person.id WHERE pfapp_person.email ='{email}' AND pfapp_person.pwd='{pwd}' LIMIT 1 ")
            c.cursor.row_factory = rfact
            user = c.fetchone()

        # If user exist, then a session is created.
        if user:
            request.session['usr'] = {'id': user['id'], 'email': email, 'type': user['type'],'name': user['name'], 'country': user['country'], 'locality': user['locality'], 'phoneno':user['phoneno']}
            return True
        else:
            messages.info(request, 'Invalid emailID or Password')
            return HttpResponseRedirect('/', request)

def logout(request):
    if checkuser(request):
        if request.session.has_key('usr'):
            del request.session['usr']
        return HttpResponseRedirect('/', request)
    else:
        messages.info(request, 'Login now to perform this action!')
        return HttpResponseRedirect('/', request)

def signup(request):
    d = loader.get_template("signup.html")
    signup_page = 'true'
    msg = ''
    stat = ''
    dv = {}
    snd = False
    if request.method == "POST":

        if 'btncnf' in request.POST:

            if request.session.has_key('ky'):
                otp = request.POST['otp']
                data = request.POST['hdata']

                if otp == request.session['ky']:
                    dv = json.loads(data)
                    email = dv['email']
                    pwd = request.POST['pwd']
                    user_type = "consumer"

                    c = connection.cursor()
                    sql = f"INSERT INTO pfapp_person (email,pwd,type) VALUES('{email}','{pwd}','{user_type}')"
                    c.execute(sql) # so id is primary key wewill save photo as id.png ex:-1.png,2.png,in a sepafrated folder in static
                    lrowid=c.lastrowid # will return the autoincremented primary key value for the current insert
                    c.close()
                    if lrowid:
                        if 'fimg' in request.FILES:
                            fimg = request.FILES['fimg']
                            fs = FileSystemStorage()
                            fnam = 'pfapp/static/usrimg/' + str(lrowid) + '.png'
                            if fs.exists(fnam):
                                fs.delete(fnam)
                            fs.save(fnam, fimg)
                    messages.info(request, 'Account created sucessfully!')
                    return HttpResponseRedirect('/',request)
                else:
                    stat = "Invalid OTP please verify with your mail..!"
                    dv = data
                    snd = True
            else:
                stat = "Timeout..session expired..please retry..!"


        else:
            email = request.POST['email']
            dv = {'email': email}
            sql = f"SELECT * FROM pfapp_person WHERE email='{email}' LIMIT 1"
            c = connection.cursor()  # connecting the database
            c.execute(sql)
            c.cursor.row_factory = rfact
            user = c.fetchone()
            c.close()
            if user:
                stat = 'user already exist.\n'
                stat += '\nTry login instead.'
            else:
                try:
                    ky = uuid.uuid4().hex[:6].upper() # OTP created.
                    # send mail
                    msg = "Dear Customer,\nThank you for registering with FarmersHub.\n"
                    msg += f"\n\nYour OTP is :{ky} \n please provide it in the space provided in your registartion form."
                    msg += "\n\nThanking you,\nregards,\n\nAdministrator,\nFarmersHub."
                    mail2snd = EmailMessage('OTP for FarmersHub registration', msg, to=(email,), cc=(), bcc=())
                    mail2snd.send()
                    dv = json.dumps(dv)
                    snd = True
                    request.session['ky'] = ky
                except Exception as ex:
                    print('signup mail error :', str(ex))
                    stat = "Unable to verify email address provided..please check"
    return HttpResponse(d.render({'data':dv,'snd':snd,'msg': stat, 'signup_page': signup_page}, request))
