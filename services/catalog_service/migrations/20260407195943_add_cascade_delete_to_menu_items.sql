ALTER TABLE menu_items 
DROP CONSTRAINT menu_items_restaurant_id_fkey,
ADD CONSTRAINT menu_items_restaurant_id_fkey 
    FOREIGN KEY (restaurant_id) 
    REFERENCES restaurants(id) 
    ON DELETE CASCADE;
    