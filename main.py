import image
import fitbit
import twitter


BACKGROUND_IMAGE = "bg.jpg"
OUTPUT_IMAGE = "out.jpg"

if __name__ == "__main__":
    fitbit = fitbit.FitbitAPI()

    today = fitbit.get_todays_data()
    best,lifetime = fitbit.get_lifetime_stats().values()
    activities = fitbit.get_activites()
    
    twitterAPI = twitter.TwitterAPI()
    follower_images = twitterAPI.get_followers()
    
    imageGenerator = image.ImageGenerator()
    imageGenerator.background(BACKGROUND_IMAGE)
    imageGenerator.write_stats(today,best,lifetime)
    imageGenerator.write_activities(activities)
    imageGenerator.draw_followers(follower_images)
    imageGenerator.save(OUTPUT_IMAGE)

    # twitterAPI.update_header(OUTPUT_IMAGE)