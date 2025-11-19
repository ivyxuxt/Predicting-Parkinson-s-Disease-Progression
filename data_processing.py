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

# extract target and features
target = :total_UPDRS
remove_cols = [:subject, :motor_UPDRS, :total_UPDRS]

features = setdiff(names(df), remove_cols)

# Train split
X_train = select(train_df, Not([:subject, :motor_UPDRS, :total_UPDRS]))
y_train = train_df[:, :total_UPDRS]

# Validation split
X_val = select(val_df, Not([:subject, :motor_UPDRS, :total_UPDRS]))
y_val = val_df[:, :total_UPDRS]

# Test split
X_test = select(test_df, Not([:subject, :motor_UPDRS, :total_UPDRS]))
y_test = test_df[:, :total_UPDRS]

println("Train set:  X_train rows = ", nrow(X_train),
        ", y_train length = ", length(y_train))

println("Val set:    X_val rows   = ", nrow(X_val),
        ", y_val length   = ", length(y_val))

println("Test set:   X_test rows  = ", nrow(X_test),
        ", y_test length  = ", length(y_test))
