# -*- coding: utf-8 -*-
# eating-humans-deadly-bet (Miya's Note). Script from miya 2026-10-09 (reworked 2026-10-24 spec; rewritten 2026-10-25 after fact check, see /mnt/project-files/eating-humans-deadly-bet/script-check.md).
SCENES = [('S01',
  'Why Is It Unthinkable?',
  'ill',
  'hook1',
  'Why does almost every society on Earth treat eating another human being as unthinkable? We usually answer with morality, religion, or simple disgust. But what if the taboo has a '
  'second root, one that runs through biology? Today we follow the science: a deadly brain disease, a strange kind of infectious protein, some uncomfortable arithmetic, and the '
  'question of whether evolution wrote a warning into our bodies.'),
 ('S02',
  'The Fore Highlands',
  'ill',
  'fore1',
  'Our story begins in the 1950s, in the eastern highlands of Papua New Guinea. The Fore people lived there, in remote mountain valleys that outsiders had barely reached. A baffling '
  'illness was taking their lives. People stumbled, shook, and lost control of their own bodies.'),
 ('S03',
  'The Laughing Death',
  'ill',
  'kuru1',
  'The Fore called it kuru, a word that means shaking or trembling. Outsiders later gave it a darker nickname: the laughing death. Patients first became unsteady on their feet. Then '
  'came tremors, slurred speech, and sudden bursts of laughter they could not control. Within months to a couple of years, they could no longer sit, swallow, or speak. Kuru was always '
  'fatal.'),
 ('S04',
  'Zigas and Gajdusek',
  'ill',
  'zigas1',
  'In 1957, a medical officer named Vincent Zigas reported the strange disease to a young American physician, Carleton Gajdusek. Together, they started asking the obvious question. '
  'What kind of illness was this? It did not look like influenza, malaria, or any known infection. There was no fever. There was no sign of bacteria. And the pattern was truly '
  'strange: kuru struck women and children far more often than adult men.'),
 ('S05',
  'A Funeral Custom',
  'ill',
  'funeral1',
  'Eventually the investigators looked at funeral customs. In the Fore community, as in some other societies, relatives of the dead sometimes performed mortuary cannibalism. '
  'Anthropologists who studied the practice describe it as an act of mourning and respect, a way to keep the dead within the family instead of leaving them to the earth. It was not '
  'hunger, and it was not violence. It was grief.'),
 ('S06',
  'Who Ate What',
  'ill',
  'shared1',
  'According to those accounts, the body was shared by custom. Men often received the muscle. Women and children were more likely to handle and eat other tissues, including the brain. '
  'And the brain, as it turned out, was where the danger was concentrated. A ritual born out of love had become a path for a disease to travel from one person to the next.'),
 ('S07',
  'A Brain Full of Holes',
  'ill',
  'sponge1',
  'When pathologists looked at the brains of kuru victims under a microscope, they saw something that looked almost impossible. The tissue was full of tiny holes. Neurons had died, '
  'and the brain had taken on the look of a sponge. Doctors now call this pattern spongiform change. And a researcher named William Hadlow noticed in 1959 that it resembled scrapie, a '
  'disease of sheep. That was an early clue.'),
 ('S08',
  'Kuru Is Infectious',
  'ill',
  'chimp1',
  "In the 1960s, Gajdusek's team tested the idea. They injected brain tissue from kuru victims into chimpanzees. After a long wait, the animals developed the same disease. Kuru was "
  'infectious. But the agent behind it survived treatments that destroy ordinary germs, and it took years to show itself. For this work, Gajdusek would share a Nobel Prize in 1976.'),
 ('S09',
  'The Prion Idea',
  'ill',
  'prion1',
  'So what was the infectious agent? For a long time, nobody knew. In the early 1980s, the neurologist Stanley Prusiner proposed an answer that many scientists found hard to believe. '
  'The agent, he said, might be made of protein alone, with no genes of its own. He gave it a name: the prion. Prusiner received the Nobel Prize in 1997, as the evidence for his idea '
  'grew stronger.'),
 ('S10',
  'A Bent Key',
  'ill',
  'key1',
  'Here is how it works. Your brain makes a normal protein called PrP, which folds into a specific shape. A prion is the same protein, folded the wrong way. Imagine a key that has '
  'been bent. The strange part is that a misfolded protein can push a normal one into the same bent shape. And then that one bends the next. The chain reaction spreads slowly, nerve '
  'cell by nerve cell.'),
 ('S11',
  'No Cure',
  'ill',
  'nocure1',
  'As the misfolded proteins pile up, brain cells die, and the tissue starts to break down. Prions resist the enzymes that normally clear away damaged proteins. That is part of why '
  'the damage cannot be stopped once it begins. There is no cure for kuru or for the other prion diseases. They are always fatal.'),
 ('S12',
  'Can You Cook It?',
  'ill',
  'cook1',
  'Now comes the question many people ask. Could you simply cook the meat and make it safe? For ordinary germs, cooking works. Salmonella and E. coli are destroyed by normal cooking '
  'temperatures, because heat unravels their proteins. But prions are different. Normal cooking does not reliably inactivate them. They can survive the chemicals used to preserve '
  'tissue, such as formaldehyde. And a standard hospital sterilizing cycle is not enough for prions, which is why hospitals use harsher protocols after surgery on a patient with a '
  'prion disease.'),
 ('S13',
  'Six Hundred Degrees',
  'ill',
  'heat1',
  'How extreme is this resistance? In a famous laboratory study from the year 2000, a team led by Paul Brown heated infected hamster brain to six hundred degrees Celsius. A small '
  'amount of infectivity still survived. It did not survive at one thousand degrees. That is a single lab experiment on one strain of hamster scrapie, but it shows how stubborn prions '
  'can be.'),
 ('S14',
  'The Silent Immune System',
  'ill',
  'immune1',
  'Your immune system also struggles here. Normally, your body spots invaders by the foreign proteins on their surface. But a prion is built from a protein your own body makes. So the '
  'immune system mounts no useful defense: no antibody response, no fever, and no early warning. The infection can travel along nerves toward the brain, while you feel completely '
  'well.'),
 ('S15',
  'Fifty Years of Waiting',
  'ill',
  'wait1',
  'And it can wait for a very long time. Kuru has one of the longest incubation periods ever documented. A study of the last kuru patients, published in 2006, found that some became '
  'ill roughly forty years after exposure, and the researchers concluded that the delay could exceed fifty years. Imagine being healthy for half a century, with a hidden infection '
  'that is already inside you.'),
 ('S16',
  'Not Every Meal Is Infected',
  'ill',
  'carry1',
  'One more point matters, and it is important to be accurate. Eating a person is not automatically a prion infection. The risk exists when the person had a prion disease. Kuru itself '
  'probably began with a rare, spontaneous prion illness in one person, and the funeral meals then passed it along. But because the danger is invisible and the delay is so long, '
  'nobody could safely tell the difference at the time.'),
 ('S17',
  'Mad Cow Disease',
  'ill',
  'mad1',
  'The world saw a related warning in Britain in the 1980s and 1990s. Cattle there were fed meat-and-bone meal made from the remains of other animals, which let a prion disease spread '
  'through the herd. The disease was called bovine spongiform encephalopathy, or mad cow disease. In 1996, a human form linked to it, variant Creutzfeldt-Jakob disease, was reported. '
  'The lesson was clear: feeding animals to their own species is dangerous.'),
 ('S18',
  'Biomagnification',
  'ill',
  'magn1',
  'Prions are only the first reason. A second comes from ecology. Scientists call it biomagnification. Some pollutants do not break down easily, so they build up in living bodies. The '
  'higher a creature sits in a food chain, the more of them it tends to carry. Mercury, certain pesticides, and other persistent chemicals collect in the tissues of top predators like '
  'sharks, and in people.'),
 ('S19',
  'A Lifetime of Chemicals',
  'ill',
  'chem1',
  'Humans eat across many levels of the food chain, and we live a long time. Our fat holds on to certain chemicals. Our liver and kidneys can store metals like cadmium. Our bones can '
  'hold lead. So the body of an adult human carries a record of what that person ate, drank, and breathed for decades.'),
 ('S20',
  'The Species Barrier',
  'ill',
  'barrier1',
  'Now consider a third protection, one that works for you every day: the species barrier. When you eat beef, chicken, or pork, most of the microbes in that meat are adapted to cows, '
  'chickens, or pigs. Their molecular keys do not fit the locks on your cells. Most of them cannot take hold in you. Cooking destroys many of the rest. That distance between species '
  'is a very real shield.'),
 ('S21',
  'When the Barrier Falls',
  'ill',
  'pathogen1',
  'The barrier shrinks when the food is a person. A pathogen that already infects humans is already tuned to human cells. Hepatitis viruses, for example, are adapted to people. And '
  'during outbreaks of Ebola, funerals where mourners handle the body have helped to spread the virus. To be fair, cooking destroys most viruses and bacteria, so the real danger is '
  'limited to what survives. But prions do survive.'),
 ('S22',
  'The Calorie Question',
  'ill',
  'calq1',
  'Did prehistoric people ever eat each other simply to survive? In 2017, the archaeologist James Cole of the University of Brighton tested that idea in the journal Scientific '
  'Reports. His approach was to calculate what a human body is actually worth in calories.'),
 ('S23',
  'What a Body Is Worth',
  'chalk',
  'calbody',
  'Cole used the numbers for an adult man weighing about sixty-six kilograms. He estimated roughly one hundred and forty-four thousand calories for the whole body. The parts people '
  'would normally eat add up to about one hundred and twenty-six thousand. The skeletal muscle, the actual meat, is only about thirty-two thousand of those. The heart offers about six '
  'hundred and fifty calories, the kidneys about three hundred and eighty, and the brain and nerves about two thousand seven hundred.'),
 ('S24',
  'Mammoth Versus Man',
  'chalk',
  'calcmp',
  'Now compare that with the animals prehistoric hunters pursued. Cole estimated that the muscle of a mammoth holds about three point six million calories. A woolly rhinoceros holds '
  "about one point two six million. Even a red deer holds about one hundred and sixty-four thousand, several times more than a single person's muscle. Cole's own comparison makes the "
  'point. If a group of twenty-five adults had only a human body to eat, the muscle would last about half a day. A mammoth could feed the same group for about two months.'),
 ('S25',
  'A Poor Food Source',
  'ill',
  'poor1',
  'So cannibalism was a poor deal as a food source. And this is exactly what Cole concluded. The low food value, he said, supports explanations that are social or cultural, not purely '
  'nutritional. That does not mean prehistoric cannibalism never happened. Archaeologists have found cut-marked human bones at many ancient sites.'),
 ('S26',
  'The Risk of the Hunt',
  'ill',
  'risk1',
  'Hunting a person is also far riskier than hunting a deer, since people fight back. That is common-sense inference, not a measured result. But the calories, the danger, and the '
  'disease risk all point the same way.'),
 ('S27',
  'Disgust as Defense',
  'ill',
  'disgust1',
  'Now let us turn to the feeling itself: disgust. We tend to treat it as a purely mental reaction. But many researchers think disgust works like a behavioral immune system. It pushes '
  'you away from things that carry disease, such as rotten food, waste, and sickness. Brain imaging studies have found that the insula, a region deep in the brain, becomes active when '
  'people feel disgust. So the shudder you feel at certain thoughts is not random. It may be doing a job.'),
 ('S28',
  'Two Imaginary Groups',
  'ill',
  'twogroups1',
  'Here is a thought experiment, and to be clear, it is an imagined scenario, not a record of real people. Picture two groups of early humans. Group A has no strong aversion to eating '
  'their dead. Group B feels an overwhelming revulsion. Over many generations, which group would you expect to suffer more from prion disease and infection? Group A, in this story, '
  'would be hit harder. Group B would stay healthier. And that difference could, over time, favor a stronger aversion.'),
 ('S29',
  'Trust and Taboo',
  'ill',
  'trust1',
  'There is another benefit. A group that refuses to treat its members as food can build stronger trust. People who see each other as allies, not as emergency rations, can hunt '
  'together and raise children together. So disgust, empathy, and taboo may have reinforced one another. We cannot prove that sequence. But it is a reasonable hypothesis, and '
  'scientists are still debating it.'),
 ('S30',
  'The PRNP Clue',
  'ill',
  'gene1',
  'Genetics adds one more intriguing clue. In 2003, a team led by the researcher Simon Mead studied a gene called PRNP, which makes the prion protein. At position 129 of that protein, '
  'people carry either of two versions. Those with one copy of each version, called heterozygotes, seemed to be better protected. Among Fore women who had survived kuru, the majority '
  'were heterozygous.'),
 ('S31',
  'Reading the Gene',
  'ill',
  'gene2',
  'The team then looked at populations all over the world. They found that the two versions are common in many regions, and they argued that this balance may reflect natural '
  'selection. Their suggestion was that deadly prion epidemics, similar to kuru, may have struck human populations in the distant past. This is an interpretation, not a proven fact, '
  'and later researchers have challenged parts of the statistical method. So treat it as a fascinating possibility.'),
 ('S32',
  'The End of Kuru',
  'ill',
  'ban1',
  'Now back to Papua New Guinea. In the late 1950s, authorities and community leaders worked to end mortuary feasting among the Fore. The ritual faded away. In the years after, kuru '
  'cases dropped. Researchers later reported that no one born after the practice ended developed the disease. The last known cases died in the 2000s, decades after the final funeral '
  'feast. That is the long shadow of a long incubation.'),
 ('S33',
  'What Kuru Taught Us',
  'ill',
  'legacy1',
  'Kuru showed medicine that an infection can be carried by a protein alone. It led to a Nobel Prize for Gajdusek and, later, one for Prusiner. And it helped scientists understand '
  'diseases like mad cow disease and other prion disorders, which are still deadly today.'),
 ('S34',
  'A Biological Logic',
  'ill',
  'logic1',
  'Prions, pollutants, the species barrier, and a poor calorie return all point the same way. The taboo is also cultural, and cultures differ. But beneath the stories we tell, there '
  'may be a quiet biological logic.'),
 ('S35',
  'The Shudder',
  'ill',
  'close1',
  'So the next time you meet cannibalism in a horror film or an old myth, remember that the scariest part may not be the monster. It may be something far smaller: a single misfolded '
  'protein, patient and invisible, bending its neighbors one by one. Nature does not always warn us loudly. Sometimes the warning is a shudder.')
]
