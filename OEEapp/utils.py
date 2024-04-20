from datetime import timedelta

def calculate_availability(available_time, unplanned_downtime):
    return ((available_time - unplanned_downtime) / available_time) * 100 if available_time != 0 else 0

def calculate_performance(ideal_cycle_time, actual_output, available_operating_time):
    return ((ideal_cycle_time * actual_output) / available_operating_time) * 100 if available_operating_time != 0 else 0

def calculate_quality(good_product_count, total_product_count):
    return (good_product_count / total_product_count) * 100 if total_product_count != 0 else 0

def calculate_oee(availability, performance, quality):
    return availability * performance * quality / 10000 