#!/user/bin/env python
#
#
#
#

import pygame
import os
import collections
import random
import re
import math
import inspect
from spritesheet import SpriteSheet

class NPCs:

	def __init__(self):

		self.OldMan = OldMan()

		self.Skeleton = Skeleton()

		self.Hermit = Hermit()

		self.npcs = collections.defaultdict()

		self._load_npcs()

	def _load_npcs(self):

		self.npcs[0] = self.OldMan

		self.npcs[8] = self.Skeleton

		self.npcs[24] = self.Hermit

class NPC:

	def __init__(self):

		self.font = pygame.font.Font("Fonts\\ttf_pixolde.ttf", 14)

		self.audio = pygame.mixer.Sound("Audio\\Misc\\talking.wav")

		self.channel = pygame.mixer.Channel(9)

		self.text = ""

		self.active = True

		self.talking = False

		self.asleep = False

		self.pause = 0

		self.pause_interval = 200

		self.sleep_interval	= 800

		self.interval = 10

		self.active_counter = 0

		self.blit_counter = 0

	@property
	def rect(self):
		return pygame.Rect(self.x, self.y, self.width, self.height)
	
	def blitme(self, screen):

		screen.blit(self.current_image, self.rect)

	def blitmetext(self, screen):

		if self.text:

			for index, line in enumerate(map(lambda x: x[0], re.findall(r"(([^ .,!?]+[ .,!?]*){0,4})", self.text)[::-1])):

				text = self.font.render(line, True, (255, 255, 255))

				screen.blit(text, (self.rect.x - text.get_width(), self.rect.y - (index)*text.get_height()))

	def reset(self):

		self.line = iter(inspect.cleandoc(random.choice(self.quotes)))
		self.blit_counter = 0
		self.pause = 0
		self.talking = False
		self.asleep = True
		self.text = ""

class OldMan(NPC):

	def __init__(self):

		super().__init__()

		self.directory = "props\\old_man.png"

		self.start_rect = (0, 0, 32, 24)

		self.x, self.y, self.width, self.height = 320, 302, 32, 24

		self.spritesheet = SpriteSheet(self.directory)

		self.image_ids = ["OldManTalk1",
						"OldManSniff",
						"OldManLookStraight",
						"OldManLookUp",
						"OldManTalk2",
						"OldManSleep1",
						"OldManSleep2",
						"OldManSleep3",
						"OldManSleep4"]

		self.images = dict(zip(self.image_ids, [pygame.transform.flip(image, True, False) for image in self.spritesheet.load_grid(self.start_rect, 3, 3, -1)]))

		self.current_image = self.images["OldManLookStraight"]

		self.quotes = ["""¿Tú también has oído la leyenda?
						¿Así que vas a conquistar a esa chica, verdad?
						¡Pues anda, ve y sube ahí!
						Je, je, je...""",

						"""—¿Has oído la legen—
						—¿Hmm?
						—¡Qué sombrero amarillo tan gracioso!
						—¿Me lo das?
						—Je, je, je...""",

						"""—Debe ser realmente especial...
						—¡Una belleza, estoy seguro!
						—Je, je, je...""",

						"""—¿Por qué dejaste de saltar?
						—¡Anda, vuelve allá arriba!
						—Je, je, je...""",

						"""Miro hacia arriba de vez en cuando.
						¡Pronto echaré un vistazo!
						Je, je, je...""",

						"""Tu tienda se ve bastante cómoda ahí...
						¿Me equivoco?
						Je, je, je...""",

						"""¿Y tú qué comes, eh?
						¡Yo prefiero las delicias de este pantano!
						¡Jo, jo, jo...!""",

						"""...ella... hmm...
						...**murmuro... ¿qué? ... eeh...
						...¿y entonces qué? ... eeh...
						...en el aire**... hmm...
						...**murmuro**... **murmuro... oh, sí...
						...¿y si...? humn...
						...eeh... comer**...
						...sí, claro... **murmuro... eeh...
						...hmm... tan alto allá arriba**...
						...¿Dónde estaba? ¡Ahh, sí!""",

						"""¡Atrapé un hada en el bosque el otro día!
						¿Quieres echar un vistazo?
						¿No?
						¡¡QUÉ LÁSTIMA!!
						Je, je, je...
						¡Esta bien, que tengas un buen día!""",

						"""¡Una vez llegué hasta donde se encontraba la chica!
						Debió de ser ella...O... Almenos eso es lo que creo...""",

						"""¿Cómo te sientes ahora mismo?
						¡Yo me siento genial ahora que estas aqui!
						Je, je, je...""",

						"""¡Oh, ojalá volver a ser joven otra vez!
						¡Entonces asi podria alcanzar a la chica en un abrir y cerrar de ojos!
						Oh, sí...""",

						"""¡Hay un lugar bonito y seguro justo encima del árbol!  
						Je, je, je...""",

						"""A diferencia de ti, ¡yo lamentablemente aprendí de mi error!  
						¡Nunca mas lo volvi a intentar de nuevo!...  
						Je, je, je...""",

						"""¡Aún tengo el deseo de algun dia poder verla!  
						¡No hay nada de malo en soñar!...  
						Je, je, je...""",

						"""¡Lo intentaré de nuevo lo aseguro!  
						Justo después de darme una siesta...""",

						"""¿Por qué razon crees que deberías continuar?  
						¿¡Acaso ya te olvidaste de la chica!?  
						Je, je, je...""",

						"""¡Deberías aceptarlo y rendirte!
						No, espera...
						¡Creo que lo lograrás, Tu puedes!
						Je, je, je...""",

						"""**Murmura Así que...** tomé prestada... esta poción de un mercader el cual encontre en el bosque,  
						¡Creo que la pocion me dio poderes especiales!  
						Je, je, je...""",

						"""That helmet seems to come in handy!
						Or is it your thick skull that cushions you when you fall?
						Hee, hee, hee...""",

						"""What is the colour of her hair?
						The leaves on that tree are red!
						Hmm...""",

						"""Could you bring me some of those red leaves?
						I like them more than the green ones!
						Hoh, hoh, hoh...""",

						"""The sewers are so clean!
						You could probably eat from the floor even!
						Yeah, I could see myself living there!
						I know, I'll go there! ... Tomorrow...""",

						"""Have you seen the flowers on top of the tree?
						Don't you think they smell good?
						Hee, hee, hee...""",

						"""Once I jumped so high that I almost got to the babe in one leap!
						That's right!
						Heh, heh, heh...""",

						"""You probably reached your peak anyways!
						Heh... Yep!""",

						"""There is a huge cabin above the sewers!
						Shouldn't be too hard to get through!
						Hee, hee, hee...""",

						"""Is that mud on your face?
						...or something else?
						Hee, hee, hee...""",

						"""Have you seen her yet?
						Pah! Didn't think so!
						Heh, heh, heh...""",

						"""She probably has a great chest -
						- full of treasure!
						Hoh, hoh, hoh...""",

						"""You seem to have been through a lot of crap!
						Heh, heh, heh...""",

						"""I heard the big house is haunted...
						Yeah, I saw a ghost there myself!
						You better watch out!
						Hoh, hoh, hoh...""",

						"""I'm just taking a break at the moment!
						You should too!
						Heh, heh, heh...""",

						"""I once caught a whiff of her!
						It must have been her...
						Hee, hee, hee...""",

						"""If I were you I'd avoid that old castle, too risky in there!
						You should take the shortcut outside!
						Heh, heh, heh...""",

						"""I heard someone fall at least a 100 times!
						Glad it wasn't me!
						Heh, heh, heh...""",

						"""I remember some beautiful meadows above the fort!
						Ah yes, flowery fields...
						Hmm...?""",

						"""How nice it was, to walk in those fields.
						If it wasn't for my age I'd be up again in no time!
						Hee, hee, hee...""",

						"""I bet the top is right above the flowery meadows!
						The babe cannot be much farther than that!
						Hoh, hoh, hoh...""",

						"""What are you going to do?
						Cry maybe?
						Heh, heh, heh...""",

						"""Instead of falling down,
						have you thought about jumping up?
						Heh, heh, heh...""",

						"""I haven't seen that magpie for a while now!
						Pity, it would have made for a good meal...
						Heh, heh, heh...""",

						"""You remind me of this really sour guy that passed by once!
						Apparently he had “calculated” a “strategy” to get the babe!
						He probably gave up too...
						Er, I mean, took a break!
						(phew!)""",

						"""His “strategy” to get the babe?
						It was something foolish like...
						Er... 
						“Not fall”
						Not very smart if you ask me!""",

						"""I came up with a new strategy to get to the babe!
						Just don't fall!
						Hoh, hoh, hoh...""",

						"""Ring the bell on the northern tower thrice, and your deepest wish is granted!
						Or was it four times?
						It's all the same to you, right?
						Heh, heh, heh...""",

						"""Have you been to the carneval yet?
						So many fun attractions!
						Heh, heh, heh...""",

						"""What's that behind you?
						So you're bringing ghosts with you down here now huh?
						What is your problem? Hmm?
						I have my right, you know!"""]

		self.line = iter(inspect.cleandoc(self.quotes[0]))

	def update(self, king):

		if self.active:

			if self.pause >= 30:

				random_int = random.randint(0, 1000)

				if random_int < 450:

					self.pause = 0

				if random_int < 50:

					self.current_image = self.images["OldManLookUp"]

				elif random_int > 100 and random_int < 150:

					self.current_image = self.images["OldManLookStraight"]

				elif random_int > 200 and random_int < 250:

					self.current_image = self.images["OldManSniff"]

				elif random_int > 300 and random_int < 350:

					self.current_image = self.images["OldManTalk1"]

				elif random_int > 400 and random_int < 450:

					self.current_image = self.images["OldManTalk2"]

				if king.y + king.height > self.y and isinstance(king.levels.levels[king.levels.current_level].npc, OldMan):

					self.pause = 0
					self.active = False
					self.talking = True

			self.pause += 1

		elif self.talking:

			try:

				if not self.blit_counter % self.interval:

					next_letter = next(self.line)

					if next_letter == "\n":

						self.blit_counter = str(self.blit_counter)

					else:

						self.text += next_letter

						if next_letter != " " and king.levels.levels[king.levels.current_level].npc:

							if isinstance(king.levels.levels[king.levels.current_level].npc, OldMan):

								self.channel.play(self.audio)


					if not self.blit_counter % (self.interval * 2):

						self.current_image = self.images["OldManTalk1"]

					else:

						self.current_image = self.images["OldManTalk2"]

				self.blit_counter += 1

			except TypeError:

				self.pause += 1

				if self.pause > self.pause_interval / 4:

					self.pause = 0
					self.blit_counter = int(self.blit_counter)
					self.text = ""

			except StopIteration:

				self.pause += 1

				if self.pause == self.pause_interval/5:

					self.current_image = random.choice([self.images["OldManTalk1"], self.images["OldManLookStraight"], self.images["OldManLookUp"]])

				if self.pause > self.pause_interval:

					self.reset()

		elif self.asleep:

			if self.blit_counter < 30:

				self.current_image = self.images["OldManTalk1"]

			elif self.blit_counter < 60:

				self.current_image = self.images["OldManSniff"]

			elif self.blit_counter < 90:

				self.current_image = self.images["OldManSleep1"]

			elif self.blit_counter < 120:

				self.current_image = self.images["OldManSleep2"]

			elif self.blit_counter < 150:

				self.current_image = self.images["OldManSleep3"]

			elif self.blit_counter < 175:

				self.current_image = self.images["OldManSleep4"]

			else:

				self.current_image = self.images["OldManSleep1"]
				self.blit_counter = 60

			self.active_counter += 1
			self.blit_counter += 1

			if self.active_counter > self.sleep_interval:

				self.asleep = False
				self.active = True

				self.active_counter = 0
				self.blit_counter = 0

				self.current_image = self.images["OldManTalk1"]

class Hermit(NPC):

	def __init__(self):

		super().__init__()

		self.directory = "props\\hermit.png"

		self.start_rect = (0, 0, 32, 32)

		self.x, self.y, self.width, self.height = 380, 312, 32, 32

		self.spritesheet = SpriteSheet(self.directory)

		self.image_ids = ["HermitTalk1",
						"HermitSwayForward",
						"HermitLookUp",
						"HermitSwayLeft",
						"HermitSwayRight",
						"HermitTalk2",
						"HermitMeditate1",
						"HermitMeditate2",
						"NA"]

		self.images = dict(zip(self.image_ids, [pygame.transform.flip(image, True, False) for image in self.spritesheet.load_grid(self.start_rect, 3, 3, -1)]))

		self.current_image = self.images["HermitMeditate1"]

		self.quotes = ["""Hmm?!
						A fellow jumper? How unusual.
						I salute you for coming this far, but I am afraid this is the end of the road for us.
						Just wait until you see what is ahead.
						I will wait here.""",

						"""Hey! Wait a minute!
						That crown..!?
						...No, it cannot be... 
						A replica, I am sure...
						You have quite the audacity, posing as the Jump King like that.
						Nevermind.
						I should warn you, up ahead is an impenetrable pass.
						Go ahead if you are curious, but I am sure we will meet again.""",

						"""When I first started there was another also attempting.
						Needless to say he didn't get as far.""",

						"""You may as well give up.
						The path ahead is impossible to traverse.""",

						"""Those jumps in the storm up there?
						Not humanly possible.""",

						"""I have studied the movements of the wind.
						It defies logic.""",

						"""If we can not reach the top.
						How could a lady ever do it?""",

						"""The thick snow prohibits calculated leaps.""",

						"""I came upon a peddler of so-called "magic boots" once.
						He never offered a shred of evidence of their supposed abilities.
						That conman must have taken me for a fool.""",

						"""If no one has been to the top,
						then where would the legend come from?""",

						"""Why do you even try?
						We will never reach the top.""",

						"""People say those statues give bad luck.
						Foolish superstition.""",

						"""If she really was at the top -
						- would someone not have found her by now?""",

						"""Face it. We will never see her.
						She is as real as a fairy or a ghost.""",

						"""Who could live in such harsh conditions?
						No, a lady could never live up there.""",

						"""There is no proof that she exists.""",

						"""Above the storm?
						Do not make me laugh.""",

						"""A chapel?
						I never expected you to be a liar.
						Disappointing."""]

		self.line = iter(inspect.cleandoc(self.quotes[0]))

	def update(self, king):

		if self.active:

			if not self.blit_counter % 20:

				if not self.blit_counter % 40:

					self.current_image = self.images["HermitMeditate1"]

				else:

					self.current_image = self.images["HermitMeditate2"]

			self.blit_counter += 1

			if king.x + king.width > self.x and isinstance(king.levels.levels[king.levels.current_level].npc, Hermit):

				self.pause = 0
				self.active = False
				self.talking = True

		elif self.talking:

			try:

				if not self.blit_counter % self.interval:

					next_letter = next(self.line)

					if next_letter == "\n":

						self.blit_counter = str(self.blit_counter)

					else:

						self.text += next_letter

						if next_letter != " " and king.levels.levels[king.levels.current_level].npc:

							if isinstance(king.levels.levels[king.levels.current_level].npc, Hermit):

								self.channel.play(self.audio)

					if not self.blit_counter % (self.interval * 2):

						self.current_image = self.images["HermitTalk1"]

					else:

						self.current_image = self.images["HermitTalk2"]


				self.blit_counter += 1

			except TypeError:

				self.pause += 1

				if self.pause > self.pause_interval / 4:

					self.pause = 0
					self.blit_counter = int(self.blit_counter)
					self.text = ""

			except StopIteration:

				self.pause += 1

				if self.pause == 20:

					self.current_image = random.choice([self.images["HermitSwayRight"], self.images["HermitSwayLeft"], self.images["HermitLookUp"], self.images["HermitSwayForward"]])

				if self.pause > 90:

					self.reset()

		elif self.asleep:

			if not self.blit_counter % 20:

				if not self.blit_counter % 40:

					self.current_image = self.images["HermitMeditate1"]

				else:

					self.current_image = self.images["HermitMeditate2"]

			self.active_counter += 1
			self.blit_counter += 1

			if self.active_counter > self.sleep_interval:

				self.asleep = False
				self.active = True

				self.active_counter = 0
				self.blit_counter = 0

class Skeleton(NPC):

	def __init__(self):

		super().__init__()

		self.directory = "props\\skeleton.png"

		self.start_rect = (0, 0, 24, 24)

		self.x, self.y, self.width, self.height = 402, 246, 24, 24

		self.spritesheet = SpriteSheet(self.directory)

		self.image_ids = ["SkeletonTalk1",
						"SkeletonTalk2"]

		self.images = dict(zip(self.image_ids, self.spritesheet.load_grid(self.start_rect, 2, 1, -1)))

		self.current_image = self.images["SkeletonTalk1"]

		self.quotes = ["""...i... i... i-s it her...?
						...feel *wheeze* h... h-er touch...
						...wh-? gone?...
						...nonono... no...""",

						"""...
						...sense her... s... s-o clear...
						...each step... up high...
						...on me...""",

						"""*sniff*
						mmh... c- can it be...
						...her s... s... sc-ent...
						...another dream...""",

						"""...he... ...filthy beard...
						...never u... u-nderstood...
						...old... ...senile...""",

						"""...the l... l-ight... no...
						...that l-ight...
						...a... a-way...""",

						"""...the noise? a voice?
						...i... i-s it her?
						...go to m... m... m-eet her...
						...s... s... s-oothe me...""",

						"""...eyes piercing...
						...me? ...me... 
						...please...""",

						"""...long... s... s... s-o long...
						...h... h-er legs
						...I wish...""",

						"""...h... h-er chest...
						...haunts my mind... no...
						...can I... so pleasing...""",

						"""...babe... babe...
						...babe of legend...
						...I would...
						...belong to m... m... m-e...""",

						"""no... no... no, nonono...
						...mine... ...begone...
						...forever a... a-lways...""",

						"""...behind her... 
						...s... s-trange winds...
						...mmh... pungent...""",

						"""...told me no...
						"reason"...
						m... m-eaning... worthless...
						...doubter... h... h-ater..."""]

		self.lines = iter(inspect.cleandoc(self.quotes[0]))

	def update(self, king):

		if self.active:

			if self.pause >= 30:

				if king.x + king.width > self.x and isinstance(king.levels.levels[king.levels.current_level].npc, Skeleton):

					self.pause = 0
					self.active = False
					self.talking = True

			self.pause += 1

		elif self.talking:

			try:

				if not self.blit_counter % self.interval:

					next_letter = next(self.lines)

					if next_letter == "\n":

						self.blit_counter = str(self.blit_counter)

					else:

						self.text += next_letter

						if next_letter != " " and king.levels.levels[king.levels.current_level].npc:

							if isinstance(king.levels.levels[king.levels.current_level].npc, Skeleton):

								self.channel.play(self.audio)

					if not self.blit_counter % (self.interval * 2):

						self.current_image = self.images["SkeletonTalk1"]

					else:

						self.current_image = self.images["SkeletonTalk2"]

				self.blit_counter += 1

			except TypeError:

				self.pause += 1

				if self.pause > self.pause_interval / 4:

					self.pause = 0
					self.blit_counter = int(self.blit_counter)
					self.text = ""

			except StopIteration:

				self.pause += 1

				if self.pause == 20:

					self.current_image = self.images["SkeletonTalk1"]

				if self.pause > 90:

					self.reset()

		elif self.asleep:

			self.current_image = self.images["SkeletonTalk1"]

			self.active_counter += 1
			self.blit_counter += 1

			if self.active_counter > self.sleep_interval:

				self.asleep = False
				self.active = True

				self.active_counter = 0
				self.blit_counter = 0







