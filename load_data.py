import sys, os
import pandas as pd
import datetime

# What does this do?
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reviews.settings")

# What does setup do?
import django
django.setup()

from reviews.models import Review, Item
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password


# ==============================================================================
#                                                                 EXTRACT REVIEW
# ==============================================================================
def extract_review_from_row(review_row):
    review = Review(id = review_row["id"],
                    author = review_row["username"],
                    item = Item.objsect.get(id=review_row["item_id"]),
                    rating = review_row["rating"],
                    review = review_row["comment"],
                    pub_date = datetime.datetime.now()
                    )
    review.save()


# ==============================================================================
#                                                          EXTRACT_USER_FROM_ROW
# ==============================================================================
def extract_user_from_row(user_row):
    user = User(username = user_row["name"],
                # user.id = user_row["id"]  # id in this case should be handled automatically
                password = make_password("password") # temporary password
                )
    user.save()


# ==============================================================================
#                                                          EXTRACT_ITEM_FROM_ROW
# ==============================================================================
def extract_item_from_row(user_row):
    pass


# the main function for the script, called by the shell
if __name__ == "__main__":

    # --------------------------------------------------------------------------
    #                           Check that the script has received two arguments
    #                (the option of which Model to update and the csv file path)
    # --------------------------------------------------------------------------
    if len(sys.argv) == 3:
        option = str(sys.argv[1]).strip().lower()
        file = str(sys.argv[2]).strip()

        # ----------------------------------------------------------------------
        #                                                 Get data from the file
        # ----------------------------------------------------------------------
        print("Reading file " + file)
        try:
            data = pd.read_csv(file)
        except:
            raise RuntimeError('Could not open the file "{}"\n'.format(file) \
                               + 'please make sure it exists')

        print(data.head(10))    # Print the first 10 rows of data

        # ----------------------------------------------------------------------
        #    Determine the relevant processing function based on option selected
        # ----------------------------------------------------------------------
        # -------------------------------------------------------------- Reviews
        if option in ["review", "reviews"]:
            necessary_columns = {"id","username","item_id","rating","comment"}
            if necessary_columns.issubset(data.columns):
                processing_function = extract_review_from_row
            else:
                raise ValueError("The data in file does not match the expected columns for reviews")
        # ---------------------------------------------------------------- Items
        elif option in ["items", "item"]:
            necessary_columns = {"id", "name"}
            if necessary_columns.issubset(data.columns):
                processing_function = extract_item_from_row
            else:
                raise ValueError(
                    "The data in file does not match the expected columns for items")
        # ---------------------------------------------------------------- Users
        elif option in ["users", "user"]:
            necessary_columns = {"id", "name"}
            if necessary_columns.issubset(data.columns):
                processing_function = extract_user_from_row
            else:
                raise ValueError(
                    "The data in file does not match the expected columns for users")
        else:
            # ------------------------------------------------------------------
            #                                            Handle Incorrect Option
            # ------------------------------------------------------------------
            raise ValueError("Incorrect Option. Legal options are 'reviews', 'items' or 'users'")

        # ----------------------------------------------------------------------
        #              For each row, add that information to the django database
        # ----------------------------------------------------------------------
        data.apply(
            processing_function,
            axis=1  # 1 = row-wise
        )

        print("Done processing the data in {}".format(file))

    else:
        # ----------------------------------------------------------------------
        #                                      Handle Incorrect Use of arguments
        # ----------------------------------------------------------------------
        message = """
            Incorrect use of arguments. Correct usage is as follows

                python load_data.py option filepath

            Where option must be one of: reviews, items or users
            And filepath must be the file path to the relevant csv file based on
            the option selected.
        """
        raise ValueError(message)
