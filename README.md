# Brain-Computer-Interface-Game

## Demos

### demo UP & DOWN part 1 (w/ audio + webcam)

https://youtu.be/VDQbfN8cseo

### demo UP & DOWN part 2 (w/ audio + webcam)

https://youtu.be/z71WdvkCPH8

### demo UP

https://youtu.be/7KFotNMFdds

### demo DOWN

https://youtu.be/Es0pMXxob9k



## Program Flow

### generate_base_data.py 

![generate base data](https://user-images.githubusercontent.com/31304414/125176806-6ff59000-e18b-11eb-95c7-2fc273f4d39a.png)

### generate_new_data.py

![generate new data](https://user-images.githubusercontent.com/31304414/125176811-7257ea00-e18b-11eb-815a-41838d73fd94.png)

### game.py 

![game](https://user-images.githubusercontent.com/31304414/125176813-7421ad80-e18b-11eb-9267-db8afa63bee4.png)


## Neural Network Architectures

### Current Architecture

the diagram below depicts the architecture of the neural network currently used in the recorded demos. As I have not yet had the chance to formally learn about neural networks - as I am just finishing up my second year - this project has given me great insight on the topic;

This architecture was created primarily via experimentation. I experimented with different numbers of hidden layers and the amount of neurons within each layer. 

![Old Architecture](https://user-images.githubusercontent.com/31304414/125176830-987d8a00-e18b-11eb-902d-42e2e01a3dc6.png)

### Experimental Architecture

As I gained more knowledge and understanding on the topics of neural networks (from sources online), I recreated the next neural network architecture that I would like to experiment with. The greatest concern I had in the previous neural network architecture was that there were too many hidden layers and hence would decrease my model's accuracy.

In the next model, I plan on decreasing the number of hidden layers (which worked against me before), but in exchange I will increase the number of hidden neurons, testing my previous assumption that more hidden layers were not redundant.

![New Architecture](https://user-images.githubusercontent.com/31304414/125176831-9a474d80-e18b-11eb-84b5-74868f70e11e.png)
