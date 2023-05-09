-- table to store user information
create table if not exists project_name.users(
    id int64 generated always as identity primary key,
    username string not null,
    password string not null,
);

-- table to store disorder information
create table if not exists project_name.mental_health_disorders(
    id int64 generated always as identity primary key,
    name string not null,
    description string not null,
)