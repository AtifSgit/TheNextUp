from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .matchResult import findResult
from .models import *
import requests
from django.views import View
from datetime import datetime, timedelta
from datetime import date
import datetime
import re

from calendar import monthrange
from django.utils import timezone

def monthsToint(month):
    months = {
        'January': '01',
        'February': '02',
        'March': '03',
        'April': '04',
        'May': '05',
        'June': '06',
        'July': '07',
        'August': '08',
        'September': '09',
        'October': '10',
        'November': '11',
        'December': '12'
    }

    return months[month]




def calendar():
    today = date.today()
    month = today.month
    year = today.year
    last_day_of_month = monthrange(year, month)[1]
    days = [day for day in range(1, last_day_of_month + 1)]
    monthsnum = [month for month in range(1, 13)]
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    # years = [year for year in range(year, year+20)]
    years = [year]
    dates = []
    current_date = date(year, month, 1)
    last_day = date(year, month, 1) + timedelta(days=31)
    while current_date.month == month:
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
        if current_date == last_day:
            break
    return days, today, dates, months,years



def getVidSuggestion(skey):
    # Set up the YouTube Data API endpoint URL
    api_url = "https://www.googleapis.com/youtube/v3/search"

    searchkey = skey

    

    # Set up the search query parameters
    params = {
        "part": "id,snippet",
        "channelId": ["UCsH9CrSfzknNKKwS6wGCeQQ","UC5SQGzkWyQSW_fe-URgq7xw","UC9xRcqG8V6yNi6Hum92EoGg"],
        "q": searchkey,
        "type": "video",
        "maxResults": 4,
        "key": "AIzaSyDdlQBcR6HSwgIB7fL9ix-JgPqr7FtWWtA",
    }

    # Send the API request and retrieve the response
    response = requests.get(api_url, params=params)

    # Parse the response JSON and print the found videos
    for item in response.json()["items"]:
        video_title = item["snippet"]["title"]
        thumbnail_url = item["snippet"]["thumbnails"]["high"]["url"]
        video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        channel_name = item["snippet"]["channelTitle"]
        # print(video_title,"\n",video_url,"\n",thumbnail_url,"\n",channel_name)


# Create your views here.


def signin(request):

    if request.method == "POST":
        if request.POST.get("formFor") == 'signingIn':
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username = username, password = password)

            if user is not None:
                login(request,user)
                return redirect(index)
                
            else:
                messages.error(request, "Wrong Credentials!", extra_tags="signin")
                return HttpResponseRedirect(request.path_info)

    
    if request.POST.get("formFor") == 'signingUp':
        # print("error")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        user = User.objects.filter(username = username)

        if user.exists():
            messages.error(request, "User already exists! Choose a different username", extra_tags="signup")
            return HttpResponseRedirect(request.path_info)
        else:
            if password1 != password2:
                messages.warning(request, "Retyped Password did not match. Please try again", extra_tags="signup")
                return HttpResponseRedirect(request.path_info)
            else:
                user = User.objects.create(username = username, email=email)
                user.set_password(password1)
                user.save()
                user = authenticate(username = username, password = password1)
                login(request,user)
                return redirect(index)
        


    return render(request, 'components/login.html')

@login_required(login_url='/login')
def index(request):


    times = ['12:00', '12:15', '12:30', '12:45', '01:00', '01:15', '01:30', '01:45', '02:00', '02:15', '02:30', '02:45', '03:00', '03:15', '03:30', '03:45', '04:00', '04:15', '04:30', '04:45', '05:00', '05:15', '05:30', '05:45', '06:00', '06:15', '06:30', '06:45', '07:00', '07:15', '07:30', '07:45', '08:00', '08:15', '08:30', '08:45', '09:00', '09:15', '09:30', '09:45', '10:00', '10:15', '10:30', '10:45', '11:00', '11:15', '11:30', '11:45', '12:00', '12:15', '12:30', '12:45', '01:00', '01:15', '01:30', '01:45', '02:00', '02:15', '02:30', '02:45', '03:00', '03:15', '03:30', '03:45', '04:00', '04:15', '04:30', '04:45', '05:00', '05:15', '05:30', '05:45', '06:00', '06:15', '06:30', '06:45', '07:00', '07:15', '07:30', '07:45', '08:00', '08:15', '08:30', '08:45', '09:00', '09:15', '09:30', '09:45', '10:00', '10:15', '10:30', '10:45', '11:00', '11:15', '11:30', '11:45']


    


    # today = datetime.today()
    today = timezone.now()
    month = today.month
    year = today.year
    last_day_of_month = monthrange(year, month)[1]
    days = [day for day in range(1, last_day_of_month + 1)]

    # days,today,dates = calendar()
    days,today,dates,months,years = calendar()

    
    calTasks = ClaendarTask.objects.all().order_by("taskDate")


    sessionbs = Session.objects.filter().all()
    sessions = DailySession.objects.filter().all()
    sessionForTask = ClaendarTask.objects.filter().all()
    # choices = scoice.sessionFor
    # print(sessions.session1_end)
    # print("999999999999999999999")
    # for sr in sessionForTask:
    #     print(sr)
    # print("999999999999999999999")

    try:
        calT2 = ClaendarTask.objects.get(taskDate=today)
        todaysessions = DailySession.objects.get(sessionFor=calT2)
        sessionFor = DailySession.objects.filter().all()
    except:
        todaysessions = None
        sessionFor = None
        messages.error(request, "No session found for today!", extra_tags='session')
    

    # try:
    #     calT2 = ClaendarTask.objects.get(taskDate=today)
    #     sessions = DailySession.objects.get(sessionFor=calT2)
    # except:
    #     sessions = None
    #     messages.error(request, "No session found for today!", extra_tags='session')
    # print(sessionbs)

    dSessionInstance = DailySession()


    if request.method == "POST":
        if request.POST.get("formFor") == "addDailysession":
            sessionforcalendar = request.POST.get("sessionto")
            session1name = request.POST.get("session1")
            session2name = request.POST.get("session2")
            session3name = request.POST.get("session3")
            s1Start = request.POST.get("s1Start")
            s2Start = request.POST.get("s2Start")
            s3Start = request.POST.get("s3Start")
            s1Start = datetime.datetime.strptime(s1Start, '%H:%M').time() 
            s2Start = datetime.datetime.strptime(s2Start, '%H:%M').time() 
            s3Start = datetime.datetime.strptime(s3Start, '%H:%M').time() 
            s1End = request.POST.get("s1End")
            s2End = request.POST.get("s2End")
            s3End = request.POST.get("s3End")
            s1End = datetime.datetime.strptime(s1End, '%H:%M').time() 
            s2End = datetime.datetime.strptime(s2End, '%H:%M').time() 
            s3End = datetime.datetime.strptime(s3End, '%H:%M').time()

            cltaskQuery = sessionforcalendar.split("on")[0].strip()
            match = re.search(r"\d{4}-\d{2}-\d{2}", sessionforcalendar)

            if match:
                date_string = match.group(0)
                # print(date_string)  # output: "2023-03-19"
            # else:
                # print("No date found in string")

            # print(cltaskQuery)
            date_string = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
            # print(date_string)
            # print(100000000000)

            getTask = Task.objects.get(taskName= cltaskQuery)
            
            cltask = ClaendarTask.objects.get(taskDate=date_string)
            dSessionInstance.sessionFor = cltask
            dSessionInstance.session1_name = Session.objects.get(session_name=session1name)
            dSessionInstance.session2_name = Session.objects.get(session_name=session2name)
            dSessionInstance.session3_name = Session.objects.get(session_name=session3name)
            dSessionInstance.session1_start = s1Start
            dSessionInstance.session2_start = s2Start
            dSessionInstance.session3_start = s3Start
            dSessionInstance.session1_end = s1End
            dSessionInstance.session2_end = s2End
            dSessionInstance.session3_end = s3End
            dSessionInstance.save()
            return redirect(index)

        return redirect(index)





    # print(calT2)
    # print(calTasks)
    addtoTask = ClaendarTask()
    tasks = Task.objects.filter().all()
    # print(sessions)

    if request.method == "POST":
        # print("Request Method POST")
        taskfor = request.POST.get("taskfor")
        taskDate = request.POST.get("taskdate")
        taskMonth = request.POST.get("taskmonth")
        # print(taskMonth)
        taskMonth = monthsToint(taskMonth)
        # print(taskMonth)
        taskYear = request.POST.get("taskyear")

        taskWhen = taskYear + "-" + taskMonth + "-" + taskDate
        taskWhen = datetime.datetime.strptime(taskWhen, '%Y-%m-%d').date() 

        # print("dhffhdfh",taskWhen)


        taskTo = Task.objects.filter(taskName=taskfor).first()
        taskIcon = TaskIconSetter.objects.get(taskFor=taskTo)
        taskSave = ClaendarTask(task= taskTo, taskDate=taskWhen,taskIcon=taskIcon)
        taskSave.save()
        return redirect(index)


        # return redirect(addTask(request,taskfor,taskDate))
    
    month = today.month
    months = months[month-1:]
    days = days[today.day-1:]
    month = '{:02d}'.format(month)
    year = str(today.year)
    # print(month)
    # print(year)
    almostDate = year+"-"+month
    # print("----------")
    # print(type(almostDate))
    # print(date(2023,3,3))

    listOfBads = []
    dictBad = {
        "morefouls": None,
        "moreOffShots":None,
        "lessOnShots":None,
        "lessCATK":None,
        "lessPossession":None,
        "moreoffsides":None,
    }
    stats = MatchResult.objects.filter().order_by('-added')[:1]
    for stat in stats:
        frm = int((stat.fouls_rm / (stat.fouls_opp+stat.fouls_rm))*100)
        fopp = int((stat.fouls_opp / (stat.fouls_opp+stat.fouls_rm))*100)

        if frm > fopp:
            listOfBads.append(frm)
            dictBad["morefouls"] = frm
        
        offrm = int((stat.offsides_rm / (stat.offsides_opp+stat.offsides_rm))*100)
        offopp = int((stat.offsides_opp / (stat.offsides_opp+stat.offsides_rm))*100)

        if offrm > offopp:
            listOfBads.append(offrm)
            dictBad["moreoffsides"] = offrm
        
        sontrm = int((stat.shootsOnTarget_rm / (stat.shootsOnTarget_opp+stat.shootsOnTarget_rm))*100)
        sontopp = int((stat.shootsOnTarget_opp / (stat.shootsOnTarget_opp+stat.shootsOnTarget_rm))*100)

        if sontrm < sontopp:
            listOfBads.append(sontrm)
            dictBad["lessOnShots"] = sontrm
    
        soffrm = int((stat.shootsOffTarget_rm / (stat.shootsOffTarget_opp+stat.shootsOffTarget_rm))*100)
        soffopp = int((stat.shootsOffTarget_opp / (stat.shootsOffTarget_opp+stat.shootsOffTarget_rm))*100)

        if soffrm > soffopp:
            listOfBads.append(soffrm)
            dictBad["moreOffShots"] = soffrm
    

        catkrm = int((stat.counterAttack_rm / (stat.counterAttack_opp+stat.counterAttack_rm))*100)
        catkopp = int((stat.counterAttack_opp / (stat.counterAttack_opp+stat.counterAttack_rm))*100)

        if catkopp > catkrm:
            listOfBads.append(catkrm)
            dictBad["lessCATK"] = catkrm

        posrm = int((stat.possession_rm / (stat.possession_opp+stat.possession_rm))*100)
        posopp = int((stat.possession_opp / (stat.possession_opp+stat.possession_rm))*100)

        if posopp > posrm:
            listOfBads.append(posrm)
            dictBad["lessPossession"] = posrm
    
    for key in list(dictBad.keys()):
        if dictBad[key] is None:
            del dictBad[key]

    sorted_dictBad = dict(sorted(dictBad.items(), key=lambda x: x[1], reverse=True))
    queryDict = {k: v for i, (k, v) in enumerate(sorted_dictBad.items()) if i < 1}

    for key in queryDict:
        if "moreOffShots" in key:
            query = "How to shoot target"
        elif "lessOnShots" in key:
            query = "Shoot Accuracy"
        elif "lessCATK" in key:
            query = "Improve Counter Attack"
        elif "morefouls" in key:
            query = "Decrease Foul"
        elif "lessPossession" in key:
            query = "Keep Possession"
        elif "moreoffsides" in key:
            query = "Offside Improve"

    # print(queryDict)
    # getVidSuggestion(query)


    api_url = "https://www.googleapis.com/youtube/v3/search"

    searchkey = query
    apikey = APIKey.objects.last()
    apikey = str(apikey)

    # print(apikey)

    # Set up the search query parameters
    params = {
        "part": "id,snippet",
        "channelId": ["UCsH9CrSfzknNKKwS6wGCeQQ","UC5SQGzkWyQSW_fe-URgq7xw","UC9xRcqG8V6yNi6Hum92EoGg"],
        "q": searchkey,
        "type": "video",
        "maxResults": 4,
        "key": apikey,
    }

    # Send the API request and retrieve the response
    response = requests.get(api_url, params=params)

    # Parse the response JSON and print the found videos


    vtitle = []
    thumb = []
    vurl = []
    chname = []
    videos = []

    svdata = SuggestedVideo()

    for item in response.json()["items"]:
        video_title = item["snippet"]["title"]
        vtitle.append(video_title)
        thumbnail_url = item["snippet"]["thumbnails"]["high"]["url"]
        thumb.append(thumbnail_url)
        # print(thumbnail_url)
        thumbnail_url = thumbnail_url.replace("hqdefault","maxresdefault")
        # print(thumbnail_url)
        video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        vurl.append(video_url)
        channel_name = item["snippet"]["channelTitle"]
        chname.append(channel_name)
        video = {
            "title": video_title,
            "url": video_url,
            "thumbnail": thumbnail_url
        }
        videos.append(video)



        # videos.append([video_title, video_url, thumbnail_url])
        # print(video_title,"\n",video_url,"\n",thumbnail_url,"\n",channel_name)

    # print(videos)
    # for video in videos:
    #     print(video[0])
    #     print(video[1])
    #     print(video[2])

    context = {
        'stats':stats,
        'frm':frm,
        'fopp':fopp,
        'offrm':offrm,
        'offopp':offopp,
        'sontrm': sontrm,
        'sontopp':sontopp,
        'soffrm': soffrm,
        'soffopp':soffopp,
        'catkrm':catkrm,
        'catkopp':catkopp,
        "vtitle":vtitle,
        "thumb":thumb,
        "chname":chname,
        "videos":videos,
        "today":today,
        'dates':dates,
        'tasks':tasks,
        'calTasks': calTasks,
        'almostDate': almostDate,
        "days":days,
        'months': months,
        'years': years,
        'times':times,
        'sessions':sessions, 
        'sessionFor':sessionFor, 
        'sessionbs':sessionbs, 
        'todaysessions':todaysessions,
        'sessionForTask':sessionForTask, 

    }
    return render(request, 'pages/index.html', context)


def signout(request):
    logout(request)
    return redirect(index)


def matchResult(request):
    stats = MatchResult.objects.filter().order_by('-added')[:1]
    context = {
        'stats':stats,
    }
    return render(request, 'components/matchResult.html', context)

def settings(request):
    days,today,dates,months,years = calendar()
    year = today.year
    years = [year for year in range(year-100, year-10)]
    settings.resultLink = []
    apidb = APIKey()
    if request.method == "POST":
        if request.POST.get("formFor") == 'addResult':
            settings.resultLink.append(request.POST.get("resultLink"))
            rLink = settings.resultLink[0]
            try:
                findResult(rLink)
                messages.success(request, "Match result successfully added to the database!", extra_tags="result")
                return redirect(settings)
            except:
                messages.error(request, "Invalid Link! please provide a valid stat link", extra_tags="result")
                return redirect(settings)
    
    if request.method == "POST":
        if request.POST.get("formFor") == 'addAPI':
            apikey = request.POST.get("apikey")
            apidb.key = apikey
            try:
                apidb.save()
                messages.success(request, "API key successfully added to the database!", extra_tags="api")
                return redirect(settings)
            except:
                messages.error(request, "Invalid API key! please provide a valid API key", extra_tags="api")
                return redirect(settings)
    
    if request.method == "POST":
        if request.POST.get("formFor") == 'addPlayer':
            try:
                name = request.POST.get("playerName")
                team = request.POST.get("playerTeam")
                position = request.POST.get("playerPosition")
                played = request.POST.get("gamesPlayed")
                goals = request.POST.get("playerGoals")
                assists = request.POST.get("playerAssists")
                placeBirth = request.POST.get("placeOfBirth")
                foot = request.POST.get("prefFoot")
                photo = request.FILES['playerPhoto']
                birthDate = request.POST.get("birthdate")
                birthMonth = request.POST.get("birthmonth")
                birthMonth = monthsToint(birthMonth)
                birthYear = request.POST.get("birthyear")
                age = today.year - int(birthYear)
                birthWhen = birthYear + "-" + birthMonth + "-" + birthDate
                # print(birthWhen)
                birthWhen = datetime.datetime.strptime(birthWhen, '%Y-%m-%d').date()
                # print(birthWhen)
                savePlayer = Player(name=name,team=team,position=position,gamesPlayed=played,
                    goals=goals,assists=assists,pob=placeBirth,age=age,pfp=photo,dob=birthWhen,isPreferredFootRight=foot)
                savePlayer.save()
                messages.success(request, "Player information has successfully added to the database!", extra_tags="player")
                return redirect(settings)
            except:
                messages.error(request, "Invalid Information! Or player may already exist!", extra_tags="player")
                return redirect(settings)


    
    
    
    
    
    
    
    
    
    context = {
        "days":days,
        'months': months,
        'years': years,
    }


    return render(request, "pages/settings.html", context)


class searchPage(View):

    def get(self, request, *args, **kwargs):
        q = self.request.GET.get('q')
        players = Player.objects.filter(name__icontains=q)
        allplayers = Player.objects.filter().all()
        suggested_players = Player.objects.filter().order_by('?')[:10]
        totfound = len(players)
        totfounds = len(suggested_players)
        # print(totfounds)
        context ={
            'players':players,
            'q':q,
            'totfound':totfound,
            'suggested_players':suggested_players,
            'allplayers': allplayers,
        }

        return render(request, 'pages/search.html', context)


def addTask(request,taskfor,taskDate):
    pass
    # print("-------addTask-------")
    # print(taskfor)
    # print(taskDate)
    # print("------addTask--------")

def testPage(request):
    days,today,dates,months,years = calendar()
    calTasks = ClaendarTask.objects.all().order_by("taskDate")
    # print(calTasks)
    # print(calTasks)
    addtoTask = ClaendarTask()
    tasks = Task.objects.filter().all()

    if request.method == "POST":
        # print("Request Method POST")
        taskfor = request.POST.get("taskfor")
        taskDate = request.POST.get("taskdate")
        taskMonth = request.POST.get("taskmonth")
        # print(taskMonth)
        taskMonth = monthsToint(taskMonth)
        # print(taskMonth)
        taskYear = request.POST.get("taskyear")

        taskWhen = taskYear + "-" + taskMonth + "-" + taskDate
        taskWhen = datetime.datetime.strptime(taskWhen, '%Y-%m-%d').date() 

        # print("dhffhdfh",taskWhen)


        taskTo = Task.objects.filter(taskName=taskfor).first()
        taskIcon = TaskIconSetter.objects.get(taskFor=taskTo)
        taskSave = ClaendarTask(task= taskTo, taskDate=taskWhen,taskIcon=taskIcon)
        taskSave.save()
        return redirect(testPage)


        # return redirect(addTask(request,taskfor,taskDate))
    
    month = today.month
    months = months[month-1:]
    days = days[today.day-1:]
    month = '{:02d}'.format(month)
    year = str(today.year)
    # print(month)
    # print(year)
    almostDate = year+"-"+month
    # print("----------")
    # print(type(almostDate))
    # print(date(2023,3,3))
    # for day in days:
    #     print(type(day))


    # print(FetchTask.objects.get(taskFetch=1))

    context = {
        'days':days,
        'today':today,
        'dates':dates,
        'icon': "<i class=\"bi bi-search\"></i>",
        'tasks': tasks,
        'calTasks': calTasks,
        'almostDate': almostDate,
        'months': months,
        'years': years,
    }
    # print(today)
    # print(dates[int(today)])
    return render(request, 'pages/testingPage2.html', context)


# def calTest(request):
#     pass
    # now = datetime.now()
    # month = now.month
    # year = now.year
    # calendar = Calendar.objects.filter(month=month, year=year).first()
    # icon = TaskIconSetter()

    # if not calendar:
    #     calendar = Calendar.objects.create(month=month, year=year)
    # tasks = ClaendarTask.objects.filter(calendar=calendar)
    # # context['calendar'] = calendar
    # # context['tasks'] = tasks
    # context = {
    #     'calendar':calendar,
    #     'tasks':tasks,
    #     'icon':icon,
    # }
    # print(tasks)
    # print(calendar)
    # return render(request, 'pages/testingPage2.html',context)


def getPlayer(request,slug):
    player = Player.objects.get(slug = slug)

    access_key = 'zypfgGMeGIf8ZPudbxKoSeMEWM90m8g-K0MsZ1DCuRI'
    query = player.slug.split('-')
    query = query[0] +"%20"+ query[1]
    # print(query)
    # print(query)
    url = f'https://api.unsplash.com/search/photos?query={query}&client_id={access_key}'
    # print(url)
    response = requests.get(url)
    data = response.json()
    images = data['results']

    player_id = query
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={query}"
    # print(url)
    response = requests.get(url)
    data = response.json()
    if data['player'] is not None and len(data['player']) > 0:
        players = []
        for player2 in data['player']:
            image_url = player2['strThumb']
            image_data = requests.get(image_url).content
            players.append({'player': player2, 'image_data': image_data})
        # context = {'player': player, 'image_data': image_data}
    else:
        # context = {'player': None, 'image_data': None}
        players = None
        image_data = None

    # print(image_data)

    # print(players)

    context = {
        'player': player,
        'images': images,
        'players':players,
        'idata':image_data,
    }
    return render(request, 'pages/playerProfile.html', context)


def userSettings(request):

    user = User.objects.get(username=request.user)
    # print(user.password)

    if request.method == "POST":
        newusername = request.POST.get('username')
        newemail = request.POST.get('email')
        # newpassword = request.POST.get('password')
        try:
            user.username = newusername
            user.email = newemail
            # user.password = newpassword
            user.save()
            # usernew = authenticate(username = newusername, password = newpassword)
            # login(request, usernew)
            messages.success(request, "Information updated successfully!")
            return redirect(userSettings)
        except:
            messages.danger(request, "Something went wrong, please try again!")
            return redirect(userSettings)
        # print(newemail,newusername,newpassword)


    context = {
        "user": user,
    }


    return render(request, 'pages/user-settings.html', context)



def addTodaySession(request):


    # start_time = datetime.time(0, 0)

    # # Define the end time (11:45 PM)
    # end_time = datetime.time(23, 45)

    # # Define the time delta (15 minutes)
    # delta = datetime.timedelta(minutes=15)

    # # Create a list of datetime objects for the day
    # times = []
    # current_time = datetime.datetime.combine(datetime.date.today(), start_time)
    # while current_time.time() <= end_time:
    #     times.append(current_time.strftime("%I:%M"))
    #     current_time += delta

    times = ['12:00', '12:15', '12:30', '12:45', '01:00', '01:15', '01:30', '01:45', '02:00', '02:15', '02:30', '02:45', '03:00', '03:15', '03:30', '03:45', '04:00', '04:15', '04:30', '04:45', '05:00', '05:15', '05:30', '05:45', '06:00', '06:15', '06:30', '06:45', '07:00', '07:15', '07:30', '07:45', '08:00', '08:15', '08:30', '08:45', '09:00', '09:15', '09:30', '09:45', '10:00', '10:15', '10:30', '10:45', '11:00', '11:15', '11:30', '11:45', '12:00', '12:15', '12:30', '12:45', '01:00', '01:15', '01:30', '01:45', '02:00', '02:15', '02:30', '02:45', '03:00', '03:15', '03:30', '03:45', '04:00', '04:15', '04:30', '04:45', '05:00', '05:15', '05:30', '05:45', '06:00', '06:15', '06:30', '06:45', '07:00', '07:15', '07:30', '07:45', '08:00', '08:15', '08:30', '08:45', '09:00', '09:15', '09:30', '09:45', '10:00', '10:15', '10:30', '10:45', '11:00', '11:15', '11:30', '11:45']



    sessionbs = Session.objects.filter().all()
    sessions = DailySession.objects.filter().all()
    # print(sessions.session1_end)
    cTasks = ClaendarTask.objects.filter().all()

    try:
        calT2 = ClaendarTask.objects.get(taskDate=today)
        todaysessions = DailySession.objects.get(sessionFor=calT2)
    except:
        todaysessions = None
        messages.error(request, "No session found for today!", extra_tags='session')

    


    if request.method == "POST":
        sessionTo = request.POST.get('sessionto')
    
    context = {
        'sessions':sessions,
        'sessionbs':sessionbs,
        'todaysessions':todaysessions,
        'cTasks':cTasks,
        'times':times,
    }

    return render(request, 'components/todaysession.html')