import tests

# ---------------------------------------------- #
#                                                #
#     construct_commit_id takes a commit_id      #
#    and outputs a list of tokens of that ver    #
#                                                #
# ---------------------------------------------- #

def construct_commit_id(commit_id):
    # takes a sequence of diffs and apply them sequentially to an initial empty token to produce a list of tokens
    tokens = [""]

    diffs_list = retrieve_diffs(commit_id)

    for diff_set in diffs_list:
        tokens = apply_diffs(tokens, diffs)

    return tokens

def retrieve_diffs(commit_id):
    # takes a commit_id, chases the parent_id, and returns a list of json objects (list of dicts)
    # each json object represents one set of diffs for a specific version/commit
    diffs_list = []
    commit = model.session.query(model.Commit).filter_by(id = commit_id).one()

    # all commits before initial commit
    while commit.parent != None:
        diffs_set = commit.diffs
        diffs_list.append(diffs_set)
        commit_id = commit.parent_id
        commit = model.session.query(model.Commit).filter_by(id = commit_id).one()

    # very initial commit
    if commit.parent == None:
        diffs_set = commit.diffs
        diffs_list.append(diffs_set)
    
    diffs_list = diffs_list[::-1]

    return diffs_list

def main():
    pass

if __name__ == "__main__":
    main()