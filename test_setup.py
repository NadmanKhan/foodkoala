"""
This file is used to setup the test environment.
"""

from sqlmodel import Session

from .db import engine
from .models import Area, Restaurant, Branch, Item


if __name__ == "__main__":
    with Session(engine()) as session:
        
        # Create areas
        
        banani = Area(name="Banani", loc_lat=23.7950, loc_lon=90.4047)
        gulshan = Area(name="Gulshan", loc_lat=23.7925, loc_lon=90.4155)
        dhanmondi = Area(name="Dhanmondi", loc_lat=23.7465, loc_lon=90.3760)
        uttara = Area(name="Uttara", loc_lat=23.8759, loc_lon=90.3796)
        session.add(banani)
        session.add(gulshan)
        session.add(dhanmondi)
        session.add(uttara)
        session.commit()

        # Create restaurants
        
        kfc = Restaurant(name="KFC")
        pizza_hut = Restaurant(name="Pizza Hut")
        burger_king = Restaurant(name="Burger King")
        session.add(kfc)
        session.add(pizza_hut)
        session.add(burger_king)
        session.commit()

        # Create branches
        
        kfc_banani = Branch(restaurant_id=kfc.id, area_id=banani.id, loc_lat=23.7942, loc_lon=90.4041)
        kfc_gulshan = Branch(restaurant_id=kfc.id, area_id=gulshan.id, loc_lat=23.7925, loc_lon=90.4155)
        kfc_dhanmondi = Branch(restaurant_id=kfc.id, area_id=dhanmondi.id, loc_lat=23.7465, loc_lon=90.3760)
        kfc_uttara = Branch(restaurant_id=kfc.id, area_id=uttara.id, loc_lat=23.8759, loc_lon=90.3796)
        session.add(kfc_banani)
        session.add(kfc_gulshan)
        session.add(kfc_dhanmondi)
        session.add(kfc_uttara)
        session.commit()

        pizza_hut_banani = Branch(restaurant_id=pizza_hut.id, area_id=banani.id, loc_lat=23.7942, loc_lon=90.4041)
        pizza_hut_gulshan = Branch(restaurant_id=pizza_hut.id, area_id=gulshan.id, loc_lat=23.7925, loc_lon=90.4155)
        pizza_hut_dhanmondi = Branch(restaurant_id=pizza_hut.id, area_id=dhanmondi.id, loc_lat=23.7465, loc_lon=90.3760)
        pizza_hut_uttara = Branch(restaurant_id=pizza_hut.id, area_id=uttara.id, loc_lat=23.8759, loc_lon=90.3796)
        session.add(pizza_hut_banani)
        session.add(pizza_hut_gulshan)
        session.add(pizza_hut_dhanmondi)
        session.add(pizza_hut_uttara)
        session.commit()

        burger_king_banani = Branch(restaurant_id=burger_king.id, area_id=banani.id, loc_lat=23.7942, loc_lon=90.4041)
        burger_king_gulshan = Branch(restaurant_id=burger_king.id, area_id=gulshan.id, loc_lat=23.7925, loc_lon=90.4155)
        burger_king_dhanmondi = Branch(restaurant_id=burger_king.id, area_id=dhanmondi.id, loc_lat=23.7465, loc_lon=90.3760)
        burger_king_uttara = Branch(restaurant_id=burger_king.id, area_id=uttara.id, loc_lat=23.8759, loc_lon=90.3796)
        session.add(burger_king_banani)
        session.add(burger_king_gulshan)
        session.add(burger_king_dhanmondi)
        session.add(burger_king_uttara)
        session.commit()

        # Create items
        
        kfc_chicken = Item(restaurant_id=kfc.id, name="Chicken", price=5.0)
        kfc_fries = Item(restaurant_id=kfc.id, name="Fries", price=2.5)
        kfc_burger = Item(restaurant_id=kfc.id, name="Burger", price=3.0)
        session.add(kfc_chicken)
        session.add(kfc_fries)
        session.add(kfc_burger)
        session.commit()

        pizza_hut_pizza = Item(restaurant_id=pizza_hut.id, name="Pizza", price=10.0)
        pizza_hut_pasta = Item(restaurant_id=pizza_hut.id, name="Pasta", price=8.0)
        pizza_hut_garlic_bread = Item(restaurant_id=pizza_hut.id, name="Garlic Bread", price=4.0)
        session.add(pizza_hut_pizza)
        session.add(pizza_hut_pasta)
        session.add(pizza_hut_garlic_bread)
        session.commit()

        burger_king_burger = Item(restaurant_id=burger_king.id, name="Burger", price=3.0)
        burger_king_fries = Item(restaurant_id=burger_king.id, name="Fries", price=2.5)
        burger_king_chicken = Item(restaurant_id=burger_king.id, name="Chicken", price=5.0)
        session.add(burger_king_burger)
        session.add(burger_king_fries)
        session.add(burger_king_chicken)
        session.commit()


