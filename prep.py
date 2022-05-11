from argparse import ArgumentParser
from datetime import date
from tempfile import NamedTemporaryFile
from pprint import pprint
import csv, os, pandas

"""
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

def get_cost_center(cost_center):
    if pandas.isna(cost_center):
        return "Unknown"
    if not isinstance(cost_center, float):
        cost_center = float(cost_center)

    #[  1., 125., 571., 608.,   0.,  nan]
    cost_center_name_map = { 
        1.0:   "District Office",
        125.0: "Grade School",
        571.0: "Junior High School",
        608.0: "High School",
        0.0:   "Other"
    }

    return cost_center_name_map.get(cost_center, "Unknown")

def budget_term_date(budget_term):
    return "{}-01-01".format(budget_term.split("-", maxsplit=1)[0])

if __name__ == "__main__":
    ap = ArgumentParser()

    ap.add_argument("filename")
    ap.add_argument("-o", "--output")

    args = ap.parse_args()

    dim_cols = ['Cost Center', 'Budget Orgn', 'Budget Unit', 'Account', 'Account Title']
    amt_cols = ["2019-2020 Actual", "2020-2021 Actual",	"2021-2022 Budget", "2022-2023 Proposed"]
    all_cols = dim_cols + amt_cols

    # Remove "$-" values (happens by default here) and split "Account" and "Budget Organization" columns
    df = pandas.read_csv(args.filename) if args.filename.endswith('csv') else pandas.read_excel(args.filename)

    #df[['Account Number','Account Name']] = df.Account.str.split(pat=' - ', n=1, expand=True)
    df[['Budget Organization Number','Budget Organization Name']] = df['Budget Orgn'].str.split(pat=' - ', n=1, expand=True)

    output_filename = args.output if args.output is not None else "output.csv"

    with open(output_filename, 'w') as out_fp:
        out_cols = list(df.columns)
        for col in amt_cols:
            out_cols.remove(col)
        out_cols += ['Budget Term','Budget Year', 'Cost Center Name','Amount']

        writer = csv.DictWriter(out_fp, fieldnames=out_cols)
        writer.writeheader()

        for row in df.to_dict('records'):
            out_row_base = row.copy()
            for col in amt_cols:
                del out_row_base[col]

            for col in amt_cols:
                out_row = out_row_base.copy()

                out_row['Cost Center Name'] = get_cost_center(row['Cost Center'])
                out_row['Budget Term'] = col
                out_row['Budget Year'] = budget_term_date(col)
                out_row['Amount']      = row[col]

                writer.writerow(out_row)

