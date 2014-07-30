from tests import generate_diffs
from tests import apply_diffs

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
        tokens = apply_diffs(tokens, diff_set)

    return tokens

def retrieve_diffs(commit_id):
    # takes a commit_id, chases the parent_id, and returns a list of json objects (list of dicts)
    # each json object represents one set of diffs for a specific version/commit
    diffs_list = []
    commit = model.session.query(model.Commit).filter_by(id = commit_id).one()

    # all commits before initial commit
    while commit.parent_id != None:
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
    # testing construct_commit_id, but change commit_id to pass diffs_list and set diffs_list to diffs_list
    # before_tokens = ["Hi.", "I am a cat!", "MRRRROWWWW." "HEYO."]
    # after_tokens = ["Hi.", "MRRRROWWWW.", "HEYO.", "MEOW MEOW!"]
    # after_after_tokens = ["Kya kya!!", "MRRRROWWWW.", "Nope.", "MEOW MEOW!"]
    # after_after_after_tokens = ["OH HAYYYYYYYY"]
    # diffs1 = generate_diffs(before_tokens, after_tokens)
    # diffs2 = generate_diffs(after_tokens, after_after_tokens)
    # diffs3 = generate_diffs(after_after_tokens, after_after_after_tokens)
    # diffs_list = [diffs1, diffs2, diffs3]
    # print construct_commit_id(diffs_list)
    pass

if __name__ == "__main__":
    main()