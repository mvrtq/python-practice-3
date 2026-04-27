# Practice 6 - Variant B: Country Analysis

import os
import csv
import json


class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")

        if os.path.exists(self.filename):
            print("File found:", self.filename)
            return True
        else:
            print("Error:", self.filename, "not found. Please download the file from LMS.")
            return False

    def create_output_folder(self, folder="output"):
        print("Checking output folder...")

        if not os.path.exists(folder):
            os.makedirs(folder)
            print("Output folder created:", folder + "/")
        else:
            print("Output folder already exists:", folder + "/")


class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")

        try:
            with open(self.filename, encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    self.students.append(row)

            print("Data loaded successfully:", len(self.students), "students")
            return self.students

        except FileNotFoundError:
            print("Error: File", self.filename, "not found. Please check the filename.")
            return []

        except Exception as e:
            print("Error:", e)
            return []

    def preview(self, n=5):
        print("First", n, "rows:")
        print("-" * 30)

        for i in range(n):
            s = self.students[i]

            print(
                s["student_id"],
                "|",
                s["age"],
                "|",
                s["gender"],
                "|",
                s["country"],
                "| GPA:",
                s["GPA"]
            )

        print("-" * 30)


class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        country_counts = {}

        for s in self.students:
            country = s["country"]

            if country in country_counts:
                country_counts[country] += 1
            else:
                country_counts[country] = 1

        top_3 = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        self.result = {
            "analysis": "Country Analysis",
            "total_students": len(self.students),
            "total_countries": len(country_counts),
            "top_3_countries": [],
            "all_countries": country_counts
        }

        for country, count in top_3:
            self.result["top_3_countries"].append({
                "country": country,
                "count": count
            })

        return self.result

    def print_results(self):
        print("-" * 30)
        print("Country Analysis")
        print("-" * 30)

        print("Total students :", self.result["total_students"])
        print("Total countries :", self.result["total_countries"])

        print("-" * 30)
        print("Top 3 Countries:")

        i = 1
        for item in self.result["top_3_countries"]:
            print(i, ".", item["country"], ":", item["count"])
            i += 1

        print("-" * 30)

    def lambda_filter_analysis(self):
        print("-" * 30)
        print("Lambda / Map / Filter")
        print("-" * 30)

        try:
            high_gpa = list(filter(lambda s: float(s["GPA"]) > 3.5, self.students))
            print("Students with GPA > 3.5 :", len(high_gpa))

            gpa_values = list(map(lambda s: float(s["GPA"]), self.students))
            print("GPA values (first 5) :", gpa_values[:5])

            good_attendance = list(
                filter(lambda s: float(s["class_attendance_percent"]) > 90, self.students)
            )
            print("Students attendance > 90% :", len(good_attendance))

        except ValueError:
            print("Warning: could not convert value — skipping row.")

        except Exception as e:
            print("Error:", e)

        print("-" * 30)


class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, "w", encoding="utf-8") as f:
                json.dump(self.result, f, indent=4)

            print("Result saved to", self.output_path)

        except Exception as e:
            print("Error while saving file:", e)


fm = FileManager("students.csv")

if not fm.check_file():
    print("Stopping program.")
    exit()

fm.create_output_folder()

dl = DataLoader("students.csv")
students = dl.load()

if students:
    dl.preview()

    analyser = DataAnalyser(students)
    analyser.analyse()
    analyser.print_results()
    analyser.lambda_filter_analysis()

    saver = ResultSaver(analyser.result, "output/result.json")
    saver.save_json()