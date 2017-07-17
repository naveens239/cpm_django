import aftership as aftership

api = aftership.APIv4("8a4aab03-8132-4fae-aca8-48c054964e14")
#couriers = api.couriers.all.get()
#print couriers
#slug = 'dhl-global-mail'
#number = 'RX386462306DE'
slug = 'dtdc'
number = 'R26561823'
print api.trackings.post(tracking=dict(slug=slug, tracking_number=number, title="Title"))
print api.trackings.get(slug, number, fields=['tag','location','updated_at','checkpoint_time'])
print api.trackings.get(slug, number)

# working code to fetch courier list
# ans =  aftership.Courier.all()
# for k, v in ans.iteritems():
#      for i in range(len(v)):
#         print v[i]['slug']+" "+ v[i]['name']
       


#print  aftership.Tracking.get()
#print aftership.Tracking.get('RX386462306DE','dhl-global-mail')
#print aftership.Tracking.last_checkpoint('RX386462306DE','dhl')