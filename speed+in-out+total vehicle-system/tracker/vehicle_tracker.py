class VehicleTracker:
    def __init__(self):
        self.tracked_objects = {}  # {botsort_id: vehicle_number}
        self.next_vehicle_number = 1
        self.history = {} # {vehicle_number: [centroids]}

    def update(self, botsort_id, centroid):
        """
        Takes a BotSort ID and maps it to a permanent Vehicle Number.
        Also tracks centroid history.
        """
        if botsort_id not in self.tracked_objects:
            # New vehicle
            veh_num = self.next_vehicle_number
            self.tracked_objects[botsort_id] = veh_num
            self.history[veh_num] = []
            self.next_vehicle_number += 1
        else:
            veh_num = self.tracked_objects[botsort_id]
        
        # Keep the last 30 positions for direction analysis
        self.history[veh_num].append(centroid)
        if len(self.history[veh_num]) > 30:
            self.history[veh_num].pop(0)
            
        return veh_num
        
    def get_history(self, vehicle_number):
        return self.history.get(vehicle_number, [])
