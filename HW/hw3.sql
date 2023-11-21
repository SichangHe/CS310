use sakila;
select '1. Views';
select '(a) (20 points) Implement a View listing all the films3. For each film, the view should provide the ID, name, and the number of actors playing. ';
drop view if exists film_listing;
create view film_listing as
select film_id,
    title,
    count(distinct actor_id) as n_actor
from film
    left join film_actor using (film_id)
group by film_id,
    title;
select '(b) (20 points) Build another View using the View from Q1-a, additionally reporting how many times each film is rented4 while keeping the ID, name, and the number of actors playing. ';
drop view if exists film_listing_rented;
create view film_listing_rented as
select film_id,
    title,
    n_actor,
    count(distinct rental_id) as n_rented
from film_listing
    left join inventory using (film_id)
    left join rental using (inventory_id)
group by film_id,
    title,
    n_actor;
select '2. Functions';
select 'Devise a function returning the total number of film rents for a given, particular film category5 name. The View from Q1-b should be used in the function. ';
drop function if exists total_rent_for_category;
delimiter $$ --
create function total_rent_for_category(category_name varchar(25))
returns integer deterministic begin
declare total_rented integer;
select sum(n_rented) into total_rented
from film_listing_rented
    join film_category using (film_id)
    join category using (category_id)
where name = category_name;
return total_rented;
end $$ --
delimiter ;
select '3. Procedures';
select 'Develop6 a procedure providing a string (out or inout type) of the actors’ full names in a film with the most number of actors. The string should be in the following form where the example shows 3 actors’ full names concatenated: ’REESE KILMER; JULIA BARRYMORE; LUCILLE DEE; FAY WINSLET’ ';
drop procedure if exists actor_names_in_movie_w_most_actors;
delimiter $$ --
create procedure actor_names_in_movie_w_most_actors(out names text) begin
declare fid integer;
select film_id into fid
from film_listing
order by n_actor desc
limit 1;
select group_concat(
        concat(first_name, ' ', last_name) separator '; '
    ) into names
from film
    join film_actor using (film_id)
    join actor using (actor_id)
where film_id = 508;
end $$ --
delimiter ;
select '4. Triggers';
select 'Come up with 2 triggers that might be beneficial for the target database and implement them. ';
select 'Trigger 1: verify that the customer has email recorded and is active before they could place a rental order.';
drop trigger if exists customer_has_info_before_rental;
delimiter $$ --
create trigger customer_has_info_before_rental before insert on rental
for each row begin
declare customer_email text;
declare customer_active boolean;
select email,
    active into customer_email,
    customer_active
from customer
where customer_id = new.customer_id;
if customer_email is null then signal SQLSTATE '45000'
SET MESSAGE_TEXT = 'Customer has no email';
end if;
if not customer_active then signal SQLSTATE '45000'
SET MESSAGE_TEXT = 'Customer is not active';
end if;
end $$ --
delimiter ;
select 'This would now fail:

insert into rental(
        rental_date,
        inventory_id,
        customer_id,
        return_date,
        staff_id
    )
values (CURDATE(), 1, 592, CURDATE(), 1);
';
select 'Trigger 2: count the number of late payments of each customer.';
create table if not exists customer_late_payment_count (
    customer_id smallint not null primary key references customer,
    late_payment_count integer not null default 0
);
drop trigger if exists check_late_payment;
delimiter $$ --
create trigger check_late_payment after insert on payment
for each row begin
declare due_date datetime;
declare old_count integer;
select return_date into due_date
from new
    join rental using (rental_id);
if new.payment_date > due_date then
select late_payment_count into old_count
from new
    join customer_late_payment_count using (customer_id);
if old_count is null then
insert into customer_late_payment_count
values (new.customer_id, 1);
else
update customer_late_payment_count
set late_payment_count = old_count + 1
where customer_id = new.customer_id;
end if;
end if;
end $$ --
delimiter ;