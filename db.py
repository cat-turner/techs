import json
from geopy.distance import geodesic

# name/epochtime/location

# tsecs” field indicates the time in epoch seconds when the location was last updated

# cache to store distances that have already been calculated
calculated_distances_cache = {}

class Technician:

    latest_location = {}

    def __init__(self):
        # I imagine this would be stored in db on prod where we would be able to
        # query for the latest data point
        # but we don't have that
        # load data and find the max for each unique technician
        f = open("api_techician_response_data.json","r")
        content = json.loads(f.read())
        # find the latest location for each tech
        for item in content:
            fds = item["features"]
            for feature_data in fds:
                # iterate through each feature
                prop = feature_data["properties"]
                geo = feature_data["geometry"]
                name = prop["name"]
                stored_data = self.latest_location.get(name)
                if not stored_data:
                    # store the first data point
                    self.latest_location[name] = {"coordinates": geo["coordinates"], "tsecs": prop["tsecs"]}
                else:
                    # compare epoch time the time in the stored data, and keep the latest result
                    if prop["tsecs"] > stored_data["tsecs"]:
                        self.latest_location[name] = {"coordinates": geo["coordinates"], "tsecs": prop["tsecs"]}

    def _compute_distance(self, name, other_name):
        """Returns the distance between two techs.
        Computes the distance and stores it in the cache.
        """
        # check out cache to see if its been calculated
        d = calculated_distances_cache.get((name, other_name), None)
        if not d:
            loc_1 = self.latest_location[name]["coordinates"]
            l1 = (loc_1[1],loc_1[0])
            loc_2 = self.latest_location[other_name]["coordinates"]
            l2 = (loc_2[1],loc_2[0])
            d = geodesic(l1, l2)
            # store both ways to make it easy to lookup
            calculated_distances_cache[(name, other_name)] = d
            calculated_distances_cache[(other_name, name)] = d
        return d

    def fetch_distance(self, name, other_name=None):
        if other_name:
            return {other_name : self._compute_distance(name, other_name)}
        else:
            result = {}
            # lets assume the person wants to see everyone
            for other_name in self.latest_location.keys():
                if other_name != name:
                    result.update({other_name: self._compute_distance(name, other_name)})
            return result

    def fetch_all_distances(self):
        names = self.latest_location.keys()
        results = {}
        for name in names:
            results[name] = self.fetch_distance(name)
        return results


if __name__ == "__main__":
    print(Technician().fetch_distance("Tech 3"))