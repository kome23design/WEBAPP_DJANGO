from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from postapp.forms import Ticketform, Reviewform, profilform
from postapp.models import profilemodel, Ticket, Comment, UserFollows, ChatMessage
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value, Count, Prefetch, Q
from django.contrib.auth.models import User
from itertools import chain
from django.utils import timezone
from django.db import transaction
from django.views.decorators.http import require_POST

# Create your views here.


def ticket(request):
    if request.method=="POST":
        tic=Ticketform(request.POST, request.FILES)
        if tic.is_valid():
            tickk=tic.save(commit=False)
            tickk.user=request.user
            tickk.save()

            return redirect("postapp:post_page")
    else:
        form=Ticketform()
        return render(request, "postapp/ticket.html",{'form':form})
    
# *****************Review************************

# @login_required
# def review(request):
#     if request.method=="POST":
#         tick=Ticketform(request.POST, request.FILES)
#         rev=Reviewform(request.POST)
#         if rev.is_valid() and tick.is_valid():
#             Ticket.objects.create(user=request.user,
#                                   title=tick.cleaned_data['title'],
#                                   description=tick.cleaned_data['description'],
#                                   image=tick.cleaned_data['image']
#                                   )

#             Review.objects.create(user=request.user,
#                                   ticket=Ticket.objects.last(),
#                                 #   rating=rev.cleaned_data['rating'],
#                                 #   headline=rev.cleaned_data['headline'],
#                                   body=rev.cleaned_data['body']
#                                   )         
#             return redirect('postapp:post_page')
#     else:
#         # try:
#         #     profilePhoto = profilemodel.objects.get(user=request.user)
#         # except:
#         #     profilePhoto = None
#         form=Reviewform()
#         formtick=Ticketform()
#         return render(request,'postapp/review.html',{'form':form, 'formtick':formtick 
#                                                     # , "profilePhoto":profilePhoto
#                                                      })


@login_required
def Myposts(request):
    posts=[] 
    user_ticket=Ticket.objects.filter(user=request.user) #we create an object to filter the ticket of the user who is connected
    user_ticket=user_ticket.annotate(content_type= Value('TICKET', CharField())) #and this to add the content type which is value to the object

    user_review=Comment.objects.filter(user=request.user)
    user_review=user_review.annotate(content_type= Value('REVIEW', CharField()))

    sort_post=sorted(chain(user_review, user_ticket), key=lambda post: 
                     post.time_created, reverse=True) #the chain permits to combine both the ticket created and review, and soted to put the revtick in order of time created
    for post in sort_post:
        if post.content_type=='TICKET':
            post_dict={'is_ticket':True,
                       'tick_title':post.title,
                       'tick_description':post.description,
                       'tick_datecreated':post.time_created,
                       'tick_created':post.time_created,
                       'tick_image':post.image.url,
                       'tick_id':post.id}  #creating a list to add up to the above empty list
        else:
            tick=post.ticket
            post_dict={'is_ticket':False,
                       'tick_title':tick.title,
                       'tick_description':tick.description,
                       'tick_created':tick.time_created,
                       'tick_image':tick.image.url,
                       'rev_time':post.time_created,
                    #    'rev_headline':post.headline,
                       'rev_body':post.body,
                    #    'yellow_star':range(post.rating),
                    #    'empty_star':range(5-post.rating),
                       'rev_answer_to':post.ticket.user.username,
                       'rev_id':post.id}
        posts.append(post_dict)

    try:
        profilePhoto = profilemodel.objects.get(user=request.user)
    except:
        profilePhoto = None
    return render(request, "postapp/mypost.html", {'posts':posts 
                                                , "profilePhoto":profilePhoto
                                                 })


@login_required
def Update(request,id):
    try:
        ticket = Ticket.objects.get(pk=id)
        if ticket.user != request.user:
            return redirect('postapp:post_page')
    except Ticket.DoesNotExist:
        return redirect('postapp:post_page')

    if request.method == "POST":
        form = Ticketform(request.POST, request.FILES, instance=ticket)
        
        if form.is_valid():
            
            if not request.FILES.get('image'):
                form.instance.image = ticket.image
                
            form.save()
            return redirect('postapp:post_page')
        else:
            return render(request, 'postapp/update.html', {'form': form})

    else:
        form = Ticketform(instance=ticket)
        return render(request, 'postapp/update.html', {'form': form})
    


    # upd=Ticket.objects.get(id=id)
    # try:
    #     ticket=Ticket.objects.get(pk=id)
    #     if ticket.user!=request.user:
    #         return redirect('postapp:post_page')
    # except Ticket.DoesNotExist:
    #     return redirect('postapp:post_page') #the try is to verify if the ticket you want to update actually do exist
    
    # if request.method=="POST":
    #     form=Ticketform(request.POST, request.FILES)
    #     if form.is_valid():
    #         if 'image' not in request.FILES:
    #             form.instance.image=ticket.image #this is to enable the user to update without changing the image

    #         # Ticket.objects.create(user=request.user, 
    #         #                       title=form.cleaned_data['title'],
    #         #                       description=form.cleaned_data['description'],
    #         #                       image=form.cleaned_data['image']
    #         #                       )
            
    #         pers=form.save(commit=False) #commit=false tells the system to wait for all the infos to be enterd before saving
    #         pers.id=ticket.id
    #         pers.user=ticket.user
    #         pers.time_created=ticket.time_created
    #         pers.save()
    #         return redirect('postapp:post_page')
    # else:
    #     # try:
    #     #     profilePhoto = profilemodel.objects.get(user=request.user)
    #     # except:
    #     #     profilePhoto = None
    #     form=Ticketform(instance=ticket) #permits all the infos entered in the ticket to be displayed on the update page before editing
    #     return render(request,'postapp/update.html',{"form":form
    #                                             #    , "profilePhoto":profilePhoto
    #                                                })

@login_required
def Delete(request,id):
    dels=Ticket.objects.get(id=id)
    if request.method=="POST":
        dels.delete()
        return redirect('postapp:post_page')
    return render(request,"postapp/delete.html",{'dels':dels})

@login_required
def Editcomment(request,id):
    # upd=Ticket.objects.get(id=id)
    try:
        review=Comment.objects.get(pk=id)
        if review.user!=request.user:
            return redirect('postapp:comment_page')
    except Comment.DoesNotExist:
        return redirect('postapp:comment_page')
    
    if request.method=="POST":
        form=Reviewform(request.POST)
        if form.is_valid():
            tag=form.save(commit=False)
            tag.id=review.id
            tag.ticket=review.ticket
            tag.user=review.user
            tag.time_created=review.time_created
            tag.save()
            return redirect('postapp:mydash_page')
    else:
        form=Reviewform(instance=review)
        return render(request,'postapp/editrev.html',{"form":form})
                                                    
                                                    

@login_required
def Deletecomment(request,id):
    delt=Comment.objects.get(id=id)
    if delt.user != request.user:
        return redirect('postapp:mydash_page')
    if request.method=="POST":
        delt.delete()
        return redirect('postapp:mydash_page')
    return render(request,"postapp/deleterev.html",{'delt':delt})



@login_required
def Dashboard(request): 
    reviews=Comment.objects.all()  
    tickuser=Ticket.objects.filter(user=request.user)
    ticket_id=[tick.id for tick in tickuser] # a  list created to get all the ticket id of the user who is connected
    review_ticket_id=[rev.ticket.id for rev in reviews]  # another list created to get all ticket id from inside the model review
    rev_from_tick=Comment.objects.filter(ticket__in=list(set(ticket_id) & set(review_ticket_id))) #it is the review of the user who is connected
    # rev_user=Review.objects.filter(user=request.user).exclude(pk__in=rev_from_tick)  #to get all the ticket of the user who is connected that has not yet been reviewed. Cannot review a ticket that has already been reviewed
    # rev_user=rev_user.annotate(content_type= Value('REVIEW', CharField()))

    user_follower=UserFollows.objects.filter(user_id=request.user) #filter to get the people who follow the user who is connected
    rev_from_followers=Comment.objects.filter(user__in=[userfollow.followed_user for userfollow in user_follower]) #to get the review of all the followers
    rev_from_followers=rev_from_followers.annotate(content_type= Value('REVIEW', CharField()))  #to add the content type to object revfromfollowers
    rev_from_tick=rev_from_tick.annotate(content_type= Value('REVIEW', CharField()))

    tick_from_followers=Ticket.objects.filter(user__in=[userfollow.followed_user for userfollow in user_follower])
    tick_from_followers=tick_from_followers.annotate(content_type= Value('TICKET', CharField()))
    tickuser=tickuser.annotate(content_type= Value('TICKET', CharField()))


    tickets=Ticket.objects.annotate(
        likes_count = Count('likes'),
        dislikes_count = Count('dislikes'),
        content_type = Value('TICKET', output_field=CharField())
    ).prefetch_related(
        Prefetch('likes', queryset=User.objects.filter(pk=request.user.id)),
        Prefetch('dislikes', queryset=User.objects.filter(pk=request.user.id))
    )


    posts=sorted(chain(rev_from_followers, rev_from_tick, tick_from_followers, tickuser), key=lambda post:
                 post.time_created, reverse=True) # we then combine again all that was gotten above and put in one list then sorted

    # ticket_answer=Ticket.objects.filter(pk__in=review_ticket_id) #to get all the ticket that has already been reviewed

    try:
        profilePhoto = profilemodel.objects.get(user=request.user)
    except:
        profilePhoto = None
    return render(request, "postapp/mydash.html",{'posts':posts, "profilePhoto":profilePhoto} )
    

@login_required
def Follow(request):
    users_follow_you=[user_follow.user.username for user_follow in UserFollows.objects.filter(
        followed_user=request.user.id
    )]  #to get all the users that follows you
    users_follow=UserFollows.objects.filter(user_id=request.user)
    user_to_exclude=[user_exclude.followed_user.username for user_exclude in users_follow] # a list created containing the username of all the users that i follow
    user_to_exclude.append(request.user.username)  # also to add my own username to the list of users that i follow
    user_to_follow=User.objects.exclude(username__in=user_to_exclude) #this is to exclude all the users that i follow and to get users that i dont follow
    if request.method=="POST":
        foll=User.objects.get(pk=request.POST["foll"]) 
        if foll in user_to_follow:
            UserFollows(user=request.user, followed_user=foll).save()
    users_follow=UserFollows.objects.filter(user_id=request.user)

    try:
        profilePhoto = profilemodel.objects.get(user=request.user)
    except:
        profilePhoto = None

    return render(request, "postapp/follow.html", {'users_follow':users_follow, "user_to_follow":user_to_follow, "user_follow_you":users_follow_you, "profilePhoto":profilePhoto})

@login_required
def Unfollow(request,id):
    try:
        unfol=UserFollows.objects.get(user=request.user, followed_user=id)
    except:
        UserFollows.DoesNotExist
        return redirect("postapp:follow_page")
    if request.method=="POST":
        unfol.delete()
        return redirect("postapp:follow_page")


@login_required   
def Review_ticket(request, id):
    ticket_to_review = Ticket.objects.get(pk=id)
    if request.method == "POST":
        reviewform=Reviewform(request.POST)
        if reviewform.is_valid():
            Comment.objects.create(user=request.user,
                                  ticket = ticket_to_review,
                                #   headline = reviewform.cleaned_data['headline'],
                                #   rating = reviewform.cleaned_data['rating'],
                                  body = reviewform.cleaned_data['body'])
            return redirect("postapp:mydash_page")
    else:
        try:
            profilePhoto = profilemodel.objects.get(user=request.user)
        except:
            profilePhoto = None
        reviewform=Reviewform()
        return render(request, "postapp/revticket.html", {"ticket_to_review":ticket_to_review, "reviewform":reviewform, "profilePhoto":profilePhoto})


@login_required
def profile(request):
    if request.method=="POST":
        form=profilform(request.POST,request.FILES)
        if form.is_valid():
            prof=form.save(commit=False)
            prof.user=request.user
            if profilemodel.objects.filter(user_id=request.user.id).exists():
                for i in profilemodel.objects.filter(user_id=request.user.id):
                    i.image=prof.image
                    i.description=prof.description
                    i.gender=prof.gender
                    i.date_profile=timezone.now
                    i.save()
                    return redirect('postapp:mydash_page')
            else:
                prof.date_profile=timezone.now
                prof.save()
                return redirect('postapp:mydash_page')
            
    else:
        try:
            profilePhoto = profilemodel.objects.get(user=request.user)
        except:
            profilePhoto = None
        form=profilform()
        return render(request,'postapp/profile.html',{'form':form,'profilePhoto':profilePhoto})


def view_comment(request, id):
    list_id=[id]
    # user_tick=Ticket.objects.get(id=id) 
    user_comment=Comment.objects.filter(ticket__in=list(set(list_id))) 
    

    sort_comment=sorted(chain(user_comment), key=lambda post: 
                     post.time_created, reverse=True)
    

    return render(request, "postapp/comment.html", {'sort_comment':sort_comment })


@transaction.atomic
@require_POST
@login_required
def React_to_ticket(request, ticket_id):
    try:
        ticket=Ticket.objects.get(id=ticket_id) 
        action = request.POST.get('action')
        if action not in ['like','dislike','unlike','undislike']:
            raise ValueError('Action invalid')
        if action == 'like':
            ticket.dislikes.remove(request.user)
            ticket.likes.add(request.user)
        elif action == 'dislike':
            ticket.likes.remove(request.user)
            ticket.dislikes.add(request.user)
        elif action == 'unlike':
            ticket.likes.remove(request.user)
        elif action == 'undislike':
            ticket.dislikes.remove(request.user)
        return JsonResponse({
            'likes_count': ticket.likes.count(),
            'dislikes_count': ticket.dislikes.count()
        })
    except Exception as e: 
        return JsonResponse({'error':str(e)},
                            status=400)
    


@login_required
def chat_view(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    if not UserFollows.objects.filter(user=request.user, followed_user=recipient).exists():
        return HttpResponseForbidden("Vous ne pouvez pas discuter avec cet utilisateur")

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        if message:
            ChatMessage.objects.create(
                sender=request.user,
                receiver=recipient,
                message=message
            )
        return redirect('postapp:chat', recipient_id=recipient_id)
    
    messages = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=recipient)) |
        (Q(sender=recipient) & Q(receiver=request.user))
    ).order_by('timestamp')
    
    return render(request, 'postapp/chat.html', {
        'recipient': recipient,
        'messages': messages
    })