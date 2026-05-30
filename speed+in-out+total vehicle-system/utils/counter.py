class Counter:
    def __init__(self, line_y):
        self.line_y = line_y
        self.counted_ids = set()
        self.vehicle_directions = {} # {vehicle_number: "IN" / "OUT"}
        self.in_count = 0
        self.out_count = 0

    def check_crossing(self, vehicle_number, history):
        """
        Check if the vehicle crossed the line based on its centroid history.
        Returns the direction if crossed in this frame, otherwise None.
        """
        if vehicle_number in self.counted_ids:
            return self.vehicle_directions.get(vehicle_number)

        if len(history) < 2:
            return None

        # Check line crossing
        prev_y = history[-2][1]
        curr_y = history[-1][1]

        # Crossed from top to bottom -> IN
        if prev_y < self.line_y and curr_y >= self.line_y:
            self.in_count += 1
            self.counted_ids.add(vehicle_number)
            self.vehicle_directions[vehicle_number] = "IN"
            return "IN"

        # Crossed from bottom to top -> OUT
        elif prev_y > self.line_y and curr_y <= self.line_y:
            self.out_count += 1
            self.counted_ids.add(vehicle_number)
            self.vehicle_directions[vehicle_number] = "OUT"
            return "OUT"

        return None

    def get_total_count(self):
        return len(self.counted_ids)
