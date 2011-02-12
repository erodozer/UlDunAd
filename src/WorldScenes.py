'''

2010 Nicholas Hydock
UlDunAd
Ultimate Dungeon Adventure

Licensed under the GNU General Public License V3
     http://www.gnu.org/licenses/gpl.html

'''

#this design is borrowed from FoFiX
#it is very efficient with resources in creating scenes and
#helps make things easier when it comes to memory management


scenes = ["MainMenu", "CreateFamily", "CreateCharacter", "Maplist",
          "BattleSystem", "FamilyList", "MenuSystem", "EquipmentScene", "Town"]

def create(engine, name):

  scene = __import__(name, globals(), locals(), [name], -1)
  return getattr(scene, name)(engine = engine)
