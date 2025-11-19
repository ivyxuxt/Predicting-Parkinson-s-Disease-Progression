using CSV, DataFrames, Statistics, Random, GLMNet
using DataFrames: Not

# load data
df = CSV.read("parkinsons_updrs.csv", DataFrame)

println(describe(df, :min, :max, :median, :nmissing))

# data processing
if "subject#" in names(df)
    rename!(df, "subject#" => "subject")
end

println("Columns loaded:")
println(names(df))

# train-test-validation split
using Random
Random.seed!(15095)

subjects = unique(df.subject)
shuffled_subjects = shuffle(copy(subjects))

# split sizes
n_train = 30
n_val   = 6
n_test  = 6

train_subjects = shuffled_subjects[1:n_train]
val_subjects   = shuffled_subjects[n_train+1 : n_train+n_val]
test_subjects  = shuffled_subjects[n_train+n_val+1 : n_train+n_val+n_test]

train_df = filter(row -> row.subject in train_subjects, df)
val_df   = filter(row -> row.subject in val_subjects, df)
test_df  = filter(row -> row.subject in test_subjects, df)
