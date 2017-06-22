from .models import Review, Item, KmeansCluster
from django.contrib.auth.models import User
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np

def update_clusters():
    print("===================================== Updating CLusters")
    num_reviews = Review.objects.count()
    update_step = ((num_reviews/100)+1) * 5 # using some magic numbers here
    if True: #num_reviews % update_step == 0:
        # ----------------------------------------------------------------------
        #                               Create a sparse matrix from user reviews
        # ----------------------------------------------------------------------
        # Each element (i,j) in our matrix contains the rating of user i for
        # item j. The username for user i will be given by the position of that
        # name in our user names list.

        # List of user names. There will be a row for each user in the matrix
        all_user_names = [x.username for x in User.objects.only("username")]

        # List of item IDs. There will be a column for each item in the matrix
        all_item_ids = {x.item.id for x in Review.objects.only("item")}

        num_users = len(all_user_names)

        # Initialise the dimensions of a Dictionary Of Keys-Based sparse matrix
        # - Each user is one row
        # - Each item is one column (where the column number corresponds to the
        #   item id). So the number of columns has to be the highest id found
        #   (plus 1, for zero indexing)
        ratings_matrix = dok_matrix((num_users, max(all_item_ids)+1), dtype=np.float32)

        # Populate the sparse matrix
        for i in range(num_users):
            # Each row is a user
            user_reviews = Review.objects.filter(author=all_user_names[i])
            for user_review in user_reviews:
                # each column is the rating the user gave an item
                ratings_matrix[i,user_review.item.id] = user_review.rating

        # ----------------------------------------------------------------------
        #                                              Perform kmeans clustering
        # ----------------------------------------------------------------------
        k = int(num_users / 10) + 2    # What are these magic numbers?
        kmeans = KMeans(n_clusters=k)
        clustering = kmeans.fit(ratings_matrix.tocsr())

        # ----------------------------------------------------------------------
        #                                   Update the KmeansClusters Model data
        # ----------------------------------------------------------------------
        KmeansCluster.objects.all().delete()
        new_clusters = {i: KmeansCluster(name=i) for i in range(k)}
        for cluster in new_clusters.values(): # clusters need to be saved before referring to users
            cluster.save()
        for i,cluster_label in enumerate(clustering.labels_):
            new_clusters[cluster_label].users.add(User.objects.get(username=all_user_names[i]))


        print("===================================================================")
        print("DONE CLUSTERING")
        print("===================================================================")
        print(KmeansCluster.objects.all())
        print("===================================================================")
