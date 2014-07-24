import json
import model

def apply_diffs(text1, diffs):
    new_text = []

    i = 0
    # while there are still lines in the original text to loop through
    while i < (len(text1)):
        while len(diffs) > 0 and ((i + 1) == diffs[0].get("line") or diffs[0].get("line") == 0):
            current = diffs.pop(0)
            if current.get("cmd") == '-':
                i += 1
            elif current.get("cmd") == '+':
                new_text.append(current.get("text"))
        if 0 <= i and i < len(text1):
            new_text.append(text1[i])
            i += 1
    return new_text

def construct_text_from_commit_id(commit_id):
    # fetch all commits for the project_id
    this_commit = model.session.query(model.Commit).filter_by(id = commit_id).one()
    project_id = this_commit.project_id
    commits = model.session.query(model.Commit).filter(model.Commit.id.between(0, commit_id)).filter_by(project_id = project_id).all()
    # # grab a list of all the diffs for each commit previous until the null
    project_diffs = []
    for commit in commits:
        diffs = json.loads(commit.diffs)
        project_diffs.append(diffs)

    text = [""]
    # apply the diffs sequentially from initial to requested
    for diffs in project_diffs:
        text = apply_diffs(text, diffs)
    print ' '.join(text)

def main():
    # ""
    # "Alphabet soup. Banana. Hello. No."
    # "Banana. California. Arkansas. No."
    construct_text_from_commit_id(2)

if __name__ == "__main__":
    main()