class VehicleTracker:
    def __init__(self):
        self.tracked_objects = {}  # {botsort_id: vehicle_number}
        self.next_vehicle_number = 1
        self.history = {}  # {vehicle_number: [centroids]}
        self.track_history = self.history
        self.last_seen = {}  # {vehicle_number: frame_number}
        self.max_history_length = 60
        self.max_inactive_frames = 60

    def update(self, botsort_id, centroid, frame_number=None):
        """
        Takes a BotSort ID and maps it to a permanent Vehicle Number.
        Also tracks centroid history and last seen frame.
        """
        if botsort_id not in self.tracked_objects:
            # New vehicle
            veh_num = self.next_vehicle_number
            self.tracked_objects[botsort_id] = veh_num
            self.history[veh_num] = []
            self.next_vehicle_number += 1
        else:
            veh_num = self.tracked_objects[botsort_id]

        # Keep the last positions for direction analysis and trail drawing
        self.history[veh_num].append(centroid)
        if len(self.history[veh_num]) > self.max_history_length:
            self.history[veh_num].pop(0)

        if frame_number is not None:
            self.last_seen[veh_num] = frame_number

        return veh_num

    def get_history(self, vehicle_number):
        return self.history.get(vehicle_number, [])

    def prune_inactive(self, active_track_ids, current_frame):
        """
        Remove stale histories for vehicles that have not been seen
        for more than max_inactive_frames. This keeps memory bounded
        and removes trails after tracker timeout.
        """
        active_vehicle_numbers = {
            self.tracked_objects[tid]
            for tid in active_track_ids
            if tid in self.tracked_objects
        }

        # Update last seen for currently active vehicles if missing
        for vehicle_number in active_vehicle_numbers:
            self.last_seen[vehicle_number] = current_frame

        inactive_ids = []
        for vehicle_number, last_frame in list(self.last_seen.items()):
            if vehicle_number in active_vehicle_numbers:
                continue
            if current_frame - last_frame > self.max_inactive_frames:
                inactive_ids.append(vehicle_number)

        for vehicle_number in inactive_ids:
            self.history.pop(vehicle_number, None)
            self.last_seen.pop(vehicle_number, None)

        # Also remove stale bot sort ID mappings if the corresponding vehicle was inactive
        stale_ids = [botsort_id for botsort_id, vehicle_number in self.tracked_objects.items()
                     if vehicle_number not in self.history]
        for botsort_id in stale_ids:
            self.tracked_objects.pop(botsort_id, None)
