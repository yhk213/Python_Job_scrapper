def save_to_file(file_name, jobs): 
    file = open(f"{file_name}.csv", "w", encoding='utf-8')
    file.write("Company, Region, Position, Link\n")
    for job in jobs:
        file.write(f"{job['company']}, {job['region']}, {job['position']}, {job['link']} \n")
    file.close()
