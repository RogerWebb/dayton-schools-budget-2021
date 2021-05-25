from argparse import ArgumentParser
from tempfile import NamedTemporaryFile
from pprint import pprint
import csv, os, pandas

"""
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

cost_center_name_map = { 
    "1":   "District Office",
    "125": "Grade School",
    "571": "Junior High School",
    "608": "High School",
    "0":   "Other"
}

if __name__ == "__main__":
    ap = ArgumentParser()

    ap.add_argument("filename")
    ap.add_argument("-o", "--output")

    args = ap.parse_args()

    amt_cols = ["2018-2019 Actual", "2019-2020 Actual",	"2020-2021 Budget", "2021-2022 Proposed"]

    # Remove "$-" values (happens by default here) and split "Account" and "Budget Organization" columns
    df = pandas.read_csv(args.filename) if args.filename.endswith('csv') else pandas.read_excel(args.filename)

    df[['Account Number','Account Name']] = df.Account.str.split(pat=' - ', n=1, expand=True)
    df[['Budget Organization Number','Budget Organization Name']] = df['Budget Organization'].str.split(pat=' - ', n=1, expand=True)

    # Break out Budget Terms into Rows and leave Amount Field as Metric
    tmp_file = NamedTemporaryFile(mode='w', delete=False)

    df.to_csv(tmp_file, index=False)
    tmp_file.flush()
    tmp_file.close()

    in_fp = open(tmp_file.name, 'r')
    reader = csv.DictReader(in_fp)

    output_filename = args.output if args.output is not None else "output.csv"

    with open(output_filename, 'w') as out_fp:
        out_cols = list(df.columns)
        for col in amt_cols:
            out_cols.remove(col)
        out_cols += ['Budget Term','Cost Center Name','Amount']

        writer = csv.DictWriter(out_fp, fieldnames=out_cols)
        writer.writeheader()

        for row in reader:
            out_row_base = row.copy()
            for col in amt_cols:
                del out_row_base[col]

            for col in amt_cols:
                out_row = out_row_base.copy()

                out_row['Cost Center Name'] = cost_center_name_map.get(row['Cost Center'], 'Other')
                out_row['Budget Term'] = col
                out_row['Amount']      = row[col]

                writer.writerow(out_row)

    os.unlink(tmp_file.name)

