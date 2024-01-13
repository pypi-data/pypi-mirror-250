import streamlit as st
from __init__ import my_component


data = [
    {
       "index": 0,
       "title": "heroes",
       "heroes": [
         {
           "id": 0,
           "hero": "Zilong",
           "perc": "60%",
           "dmg":"",
           "img": "https:static.wikia.nocookie.net/mobile-legends/images/f/f3/Corrosion_Scythe.png",
         },
         {
           "id": 1,
           "hero": "Zilong",
           "perc": "60%",
           "dmg":"",
           "img": "https:static.wikia.nocookie.net/mobile-legends/images/e/ed/Feather_of_Heaven.png",
         },
       ],
     },
     {
       "index": 1,
       "title": "All Damage",
       "heroes": [
         {
           "id": 0,
           "hero": "Zilong",
           "perc": "20%",
           "dmg":"",
           "img": "https:static.wikia.nocookie.net/mobile-legends/images/f/f3/Corrosion_Scythe.png",
         },
         {
           "id": 1,
           "hero": "Zilong",
           "perc": "40%",
           "dmg":"",
           "img": "https:static.wikia.nocookie.net/mobile-legends/images/e/ed/Feather_of_Heaven.png",
         },
       ],
     },
     {
       "index": 2,
       "title": "Base Damage",
       "heroes": [
         {
           "id": 1,
           "hero": "Zilong",
           "perc": "20%",
           "dmg":"",
           "img": "https:static.wikia.nocookie.net/mobile-legends/images/f/f3/Corrosion_Scythe.png",
         },
       ],
     },
   ]

my_component(damageType=data)