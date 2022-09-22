"""Infrastructure for detecting abstraction barrier violations."""

class AbstractionViolation(Exception):
    pass

def datatype(obj):
    return type(obj).__name__

# Generic abstract data type
class Abstract(object):
    def __add__(self, other):
        raise AbstractionViolation(
            f"Can't add {datatype(self)} object to {datatype(other)}"
        )

    def __radd__(self, other):
        raise AbstractionViolation(
            f"Can't add {datatype(self)} object to {datatype(other)}"
        )

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return other is self
        raise AbstractionViolation(
            f"Can't use == on {datatype(self)} object and {datatype(other)}"
        )

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return other is not self
        raise AbstractionViolation(
            f"Can't use != on {datatype(self)} object and {datatype(other)}"
        )

    def __bool__(self):
        raise AbstractionViolation(f"Can't use {datatype(self)} object as a boolean")

    def __getitem__(self, index):
        raise AbstractionViolation(f"Can't use [] notation on {datatype(self)} object")

    def __contains__(self, other):
        raise AbstractionViolation(
            f"Can't use contains notation on {datatype(self)} object"
        )

    def __delitem__(self, other):
        raise AbstractionViolation(
            f"Can't use del notation on {datatype(self)} object"
        )

    def __iter__(self):
        raise AbstractionViolation(f"Can't iterate on {datatype(self)} object")

    def __len__(self):
        raise AbstractionViolation(
            f"Can't use len notation on {datatype(self)} object"
        )

    def __setitem__(self, key, item):
        raise AbstractionViolation(
            f"Can't use setitem notation on {datatype(self)} object"
        )

    def __call__(self, *args, **kwargs):
        raise AbstractionViolation(f"Can't call {datatype(self)} object")

    def __hash__(self):
        return id(self)

class User(Abstract):
    def __init__(self, name, reviews):
        self.a, self.b = name, {review_restaurant_name(r): r for r in reviews}
    def __repr__(self):
        return f'<User {self.a} {list(map(repr, self.b))}>'

make_user = User
user_name = lambda u: u.a
user_reviews = lambda u: u.b
user_reviewed_restaurants = lambda u, r: [r_ for r_ in r if restaurant_name(r_) in user_reviews(u)]
user_rating = lambda u, n: review_rating(user_reviews(u)[n])

class Review(Abstract):
    def __init__(self, restaurant_name, rating):
        self.a, self.b = restaurant_name, rating
    def __repr__(self):
        return f'<Review {self.a} {self.b}>'

make_review = Review
review_restaurant_name = lambda r: r.a
review_rating = lambda r: r.b

class Restaurant(Abstract):
    def __init__(self, name, location, categories, price, reviews):
        self.a, self.b, self.c, self.d, self.e = name, location, categories, price, reviews
        self.f = [review_rating(r) for r in reviews]
        self.g = len(self.e)
        self.h = sum(review_rating(r) for r in self.e) / len(self.e)
    def __repr__(self):
        return f'<Restaurant {self.a}>'

make_restaurant = Restaurant
restaurant_name = lambda r: r.a
restaurant_location = lambda r: r.b
restaurant_categories = lambda r: r.c
restaurant_price = lambda r: r.d
restaurant_ratings = lambda r: r.f

old = {}
def swap_implementations(impl, user=True, review=True, rest=True):
    # save other implementations
    old['user'] = impl.make_user, impl.user_name, impl.user_reviews, impl.user_reviewed_restaurants, impl.user_rating
    old['review'] = impl.make_review, impl.review_restaurant_name, impl.review_rating
    old['rest'] = impl.make_restaurant, impl.restaurant_name, impl.restaurant_location, impl.restaurant_categories, impl.restaurant_price, impl.restaurant_ratings

    # save our implementations
    new_user = make_user, user_name, user_reviews, user_reviewed_restaurants, user_rating
    new_review = make_review, review_restaurant_name, review_rating
    new_rest = make_restaurant, restaurant_name, restaurant_location, restaurant_categories, restaurant_price, restaurant_ratings

    # replace impl's implementations with ours
    if user:
        impl.make_user, impl.user_name, impl.user_reviews, impl.user_reviewed_restaurants, impl.user_rating = new_user
    if review:
        impl.make_review, impl.review_restaurant_name, impl.review_rating = new_review
    if rest:
        impl.make_restaurant, impl.restaurant_name, impl.restaurant_location, impl.restaurant_categories, impl.restaurant_price, impl.restaurant_ratings = new_rest

def restore_implementations(impl):
    impl.make_user, impl.user_name, impl.user_reviews, impl.user_reviewed_restaurants, impl.user_rating = old['user']
    impl.make_review, impl.review_restaurant_name, impl.review_rating = old['review']
    impl.make_restaurant, impl.restaurant_name, impl.restaurant_location, impl.restaurant_categories, impl.restaurant_price, impl.restaurant_ratings = old['rest']

def check_same_elements(cluster1, cluster2):
    return len(cluster1) == len(cluster2) and all(el1 == el2 for el1, el2 in zip(cluster1, cluster2))

def deep_check_same_elements(clusters1, clusters2):
    return len(clusters1) == len(clusters2) and all(check_same_elements(c1, c2) for c1, c2 in zip(clusters1, clusters2))

def sample(lst, k):
    return lst[:k]
