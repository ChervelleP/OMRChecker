import csv
import pandas as pd
from statistics import mean, median
from fpdf import FPDF #for pdf creation and handeling
from pathlib import Path

ANALYTICS_FILE= Path("analytics.csv")

def updateAnalytics(file_id, score):
    #logging students' score
    if not ANALYTICS_FILE.exists():
        with open(ANALYTICS_FILE, 'w', newline='') as f:
            writer=csv.writer(f)
            writer.writerow(["id", "score", "mean", "median", "max", "min"])

    df = pd.read_csv(ANALYTICS_FILE) #reading the file into the dataframe

    new_entry=pd.DataFrame({"id": [file_id], "score": [score]}) #creating a new row
    df = pd.concat([df, new_entry], ignore_index=True) #concatenate the new data into the dataframe

    scores = df["score"] #extracting the updated list

    #calculating stats
    mean_score = round(mean(scores), 2)
    median_score = round(median(scores), 2)
    max_score = round(max(scores), 2)
    min_score = round(min(scores), 2)

    #populating the dataframe
    df["mean"] = mean_score
    df["median"] = median_score
    df["max"] = max_score
    df["min"] = min_score

    df.to_csv(ANALYTICS_FILE, index=False) #updating the analytics file by overwriting it

    #printing to terminal
    print(f"[Analytics] Added {file_id} -> {score:.2f}")
    print(f"[Analytics] Class Mean: {mean_score:.2f}")
    print(f"            Median: {median_score:.2f}")
    print(f"            Max: {max_score:.2f}")
    print(f"            Min: {min_score:.2f}")

def printScoreSummary():
    #outputting satistical data
    if not ANALYTICS_FILE.exists():
        print("[Analytics] No data available.")
        return

    df = pd.read_csv(ANALYTICS_FILE)
    if df.empty:
        print("[Analytics] Analytics file is empty.")
        return

    scores = df["score"]

    print("\n[Class Summary]")
    print(f"Mean Score: {mean(scores):.2f}")
    print(f"Median Score: {median(scores):.2f}")
    print(f"Highest Score: {max(scores):.2f}")
    print(f"Lowest Score: {min(scores):.2f}\n")

    '''
    scores= []
    try:
        with open(ANALYTICS_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                scores.append(float(row[1]))
        if scores:
            print(f"[Analytics] Mean: {mean(scores):.2f}, High: {max(scores)}, Low: {min(scores)}")
    except FileNotFoundError:
        print("[Analytics] no data sourced yet!")
'''

def exportAnalyticsPDF(filename="analytics_report.pdf"):

    #checking if the file exists
    if not ANALYTICS_FILE.exists():
        print("[ANALYTICS] file not found")
        return

    #loading .csv into the pandas dataframe
    df = pd.read_csv(ANALYTICS_FILE)

    #checking if the df is empty
    if df.empty:
        print("[ANALYTICS] analytics.csv file is empty")
        return

    #initialize new doc
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times New Roman", size=12)

    #formatting:
    pdf.cell(200, 10, txt="Student Analytics Report", ln=True, align='C')
    pdf.ln(10)
    headers = list(df.columns)
    for header in headers:
        pdf.cell(30,10, txt=str(header), border=1, align='C')
    pdf.ln()

    #populating rows with student data
    for index, row in df.iterrows():
        for item in row:
            pdf.cell(30, 10, txt=str(item), border=1, align='C')
        pdf.ln

    #save and output
    pdf.output(filename)
    print(f"[Analytics] PDF report saved as {filename}")

#to run analytics.py manually:
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python analytics.py <student_id>")
        print("       python analytics.py all")
        sys.exit(1)

    command = sys.argv[1]

    if command == "summary":
        printScoreSummary()
    elif command == "report" and len(sys.argv) == 3:
        student_id = sys.argv[2]
        report = generateReport(student_id)
        for key, value in report.items():
            print(f"{key}: {value}")
    else:
        print("invalid command")


        