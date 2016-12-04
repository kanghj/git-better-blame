
import git

repo = git.Repo('/Users/darius/workspace/OfficeSimulatorThing')

fifty_first_commits = list(repo.iter_commits('master', max_count=50))

print fifty_first_commits

print 'diffs'
# TODO how to get blob content?
print [[(diffobj.change_type, diffobj.a_blob) for diffobj in commit.diff(commit.parents[0])] for commit in fifty_first_commits if len(commit.parents) > 0]

print 'parents'
print [commit.parents for commit in fifty_first_commits]

print 'blobs'

def read_blob(blob):
    return blob.data_stream.read().decode('utf-8')

print [[read_blob(blob) for blob in list(commit.tree.traverse()) if blob.type == 'blob'] for commit in fifty_first_commits]

