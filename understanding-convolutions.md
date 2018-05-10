## 走进卷积

作者：Christopher Olah 翻译：ChenBooo 原文：[Understanding Convolutions][understanding-convolutions]

在上一篇博文中，我为大家介绍了卷积神经网络的基本概念，但并没有就其中涉及的数学原理进行阐释。如果想对卷积神经网络有更加深入的理解，我们必须首先理解卷积。

如果仅仅只是想了解卷积神经网络，那么只需要对卷积有概念性的了解。但是我编写这一系列的博文，是为了帮助大家走进卷积神经网络的最前沿，去探索更多最新的技术。为了实现这个目标，必须对卷积有深入的理解。

松一口气的是，通过以下的一些例子，卷积是一个十分简单明晰的概念。


### 从扔球开始

想象我们从高处扔下一个球，球垂直下落，是一个简单的一维运动。球第一次停稳后，从原地提起，再一次扔下，两次扔球，球最后的落点距离第一个的落点距离为c的可能性有多大？

让我们详述一下实验过程。在球第一次停稳时，其位置与第一个落点的距离为`a`，其概率为`f(a)`，这里`f`是球停稳后与其第一个落点之间距离的概率分布函数。

第一次扔球完成后，我们将球从其所在位置再一次提到一定高度，然后再一次让球落下。球第二次落下后滚动的距离记为`b`，其概率为`g(b)`。如果两次抛球的高度不同，那么`g`可能是一个不同于`f`的概率分布函数。

![](/image/understanding_convolutions/ProbConv-fagb.png)

如果我们取第一次球滚动的距离为定值`a`，为了保证两次抛球滚动的总距离`c`不变，那么第二次抛球滚动的距离也须为定值`b`，才能使`a+b=c`成立。而出现此特定的`a`和`b`的概率也很直观，为`f(a)g(b)`<a href="#comments1"><sup>[1]</sup></a>

让我们从具体的例子来理解。我们想要两次抛球总滚动距离为3。如果第一次抛球`a=2`，那么第二次抛球需要滚动`b=1`才能达到我们的要求。其出现概率为`f(2)⋅g(1)`。

![](/image/understanding_convolutions/ProbConv-split-21.png)

值得注意的是，以上不是唯一可以达到总距离为3的组合。球可以第一次滚动1，第二次滚动2；或者第一次滚动0，第二次滚动3；或者其他任意`a`和`b`的组合，只要满足`a+b=3`即可。

![](/image/understanding_convolutions/ProbConv-splits-12-03.png)

其对应的概率依次为`f(1)⋅g(2)`,` f(0)⋅g(3)`等等。

为了找出两球滚动总距离为c的概率，我们不能仅仅只考虑一种可能的组合，而必须考虑所有和为c的组合，然后将这些组合的概率相加。

<center>...  f(0)⋅g(3) + f(1)⋅g(2) + f(2)⋅g(1)  ...</center>

我们已经知道对每一个满足`a+b=c`的组合，其概率为`f(a)⋅g(b)`。所以通过将所有满足`a+b=c`的组合的发生概率相加，我们就能得到两次抛球总的滚落距离为`c`的概率为：

![](/image/understanding_convolutions/f1.png)

结果是，我们正在进行一个卷积计算！更确切的说，计算`c`点，函数`f`和`g`的卷积定义如下：

![](/image/understanding_convolutions/f2.png)

如果我们取`b=c−a`，那么可以得到：

![](/image/understanding_convolutions/f3.png)

这就是卷积的标准定义<a href="#comments2"><sup>[2]</sup></a>。

为了使概念更加具体。我们从球可能的落点来思考。在第一次扔球之后，球会落在一个中间位置`a`，概率为`f(a)`。而如果球第一次落在`a`，那么它就有`g(c−a)`的概率最后落在位置`c`。

![](/image/understanding_convolutions/ProbConv-OnePath.png)

为了计算它的卷积，我们需要考虑所有的中间位置。

![](/image/understanding_convolutions/ProbConv-SumPaths.png)

### 图解卷积

这里有一个帮助更容易理解卷积的技巧。

首先，很容易观察的是，假设一个球从起点滚动距离`x`的概率为f(x)，那么球再从终点滚落回原本的起点的概率则为`f(−x)`。

![](/image/understanding_convolutions/ProbConv-Reverse.png)

如果我们已经知道第二次扔球后球落在位置`c`，那么球在之前一次落下时停在位置`a`的概率是多大呢？

![](/image/understanding_convolutions/ProbConv-BackProb.png)

所以之前一次落在位置`a`的概率是`g(−(a−c))=g(c−a)`。

现在，考虑球最终停在位置`c`，所对应的每一个可能的中间位置的概率。我们已经知道球第一次落在位置`a`的概率为`f(a)`，也知道，如果最终落在位置`c`时，其前一次落在位置`a`的概率为`g(c−a)`

![](/image/understanding_convolutions/ProbConv-Intermediate.png)

将所有可能的`a`加起来，我们就得到了卷积。

这个方法的优点在于，给了我们一个将卷积计算可视化的途径。我们可以用一张图来表示对于值`c`的卷积计算过程。通过调整图中底部的标尺，我们就可以计算不同`c`值的卷积。这让我们可以建立对卷积的整体认识。

例如，我们可以发现在上下的分布对齐时，其卷积达到最大值。

![](/image/understanding_convolutions/ProbConv-Intermediate-Align.png)

当分布之间相交减小时，其卷积值收缩。

![](/image/understanding_convolutions/ProbConv-Intermediate-Sep.png)

使用该技巧制作动画，可以通过可视化的方式直观的理解卷积。

下图，是我们对两个矩形窗函数的可视化卷积计算：

![](/image/understanding_convolutions/Wiki-BoxConvAnim.gif)

有了上面的认识，许多事件就变的更直观了。

现在考虑一个非概率的例子。对音频的处理有时会使用卷积。例如，人们可能会使用一个带有两个尖峰，但是在其他地方值都是零的函数，以创建一个回声。随着我们的双尖峰函数的滑动，一个尖峰先到达一个时间点，将该信号添加到输出声音，然后另一个尖峰到达，添加第二个延迟的副本。

### 高纬度卷积

卷积是一个十分通用的概念，不止应用于一维数据，也可以应用与更高维度的数据上。

仍然以抛球为例。这次我们考虑球落下的位置不是在一维的线上，而是在二维平面上。

![](/image/understanding_convolutions/ProbConv-TwoDim.png)

卷积的计算与之前完全相同：

![](/image/understanding_convolutions/f4.png)

唯一不同的是，现在`a`,`b`和`c`变成了向量，所以更清楚的描述变为：

![](/image/understanding_convolutions/f5.png)

或者其标准的定义表达式：

![](/image/understanding_convolutions/f6.png)

与一维卷积相同，我们将二维卷积视为一个函数在另一个函数之上滑动，然后相乘、相加。

二维卷积一个常见的应用是图像处理。我们可以将图像视作二维函数。许多重要的图像转换函数使用卷积，通过将图片与一个很小的，本地的核函数做卷积。

![](/image/understanding_convolutions/RiverTrain-ImageConvDiagram.png)

核依次滑过图像的每一个位置，并且对其覆盖的像素进行加权求和，其结果作为新像素的值。

例如，通过取3x3内所有像素的平均值，我们可以模糊一张图片。为了实现该效果，我们的核函数只需要每个像素取值为1/9即可。

![](/image/understanding_convolutions/Gimp-Blur.png)

通过取相邻两像素为-1和1，其他像素取0，我们可以用其检测出图中的边界。其原理是，通过与核函数做卷积，我们得到所有相邻像素之间的差值。当相邻像素变化很小时，其差值约等于零。而对于图中的边界，其相邻像素的值在其边界的垂直方向上差值很大。

![](/image/understanding_convolutions/Gimp-Edge.png)

在gimp文档中还有更多关于图像处理的[例子][example]

### 卷积神经网络

最后，卷积怎样关联到卷积神经网络呢？

以一维的卷积层为例，其输入` {xn}`，输出为`{yn}`，如在上一篇[文章][eassay]中所述：

![](/image/understanding_convolutions/Conv-9-Conv2-XY.png)

如所看到的，我们可以将输出用输入描述为：
<center>yn=A(xn,xn+1,...)</center>

一般来说，`A`表示多个神经元。简单起见，先考虑此处只有一个神经元的情况。神经网络中对神经元的一个典型描述为：
<center>σ(w0x0+w1x1+w2x2 ... +b)</center>

这里的`x0, x1…`是输入，权重`w0, w1, …`描述了神经元与输入之间的关系。一个负的权重意味着其对于的输入抑制神经元，而一个正的权重则激发神经元。权重是神经元的核心，控制这神经元的行为<a href="#comments3"><sup>[3]</sup></a>。如果多个神经元有相同的权重值，则这些神经元就是完全相同的。

这是神经元的布线，描述了卷积将为我们处理的所有重量和判断哪些是相同的。

通常，我们一次性描述一个层中的所有神经元，而不是单独描述每一个神经元。其中的技巧就是使用一个权重矩阵， `W`：
<center>y=σ(Wx+b)</center>

例如，我们有：
<center>y0=σ(W0,0x0+W0,1x1+W0,2x2...)</center>
<center>y1=σ(W1,0x0+W1,1x1+W1,2x2...)</center>

矩阵中的每一行都表示一个与其输入相关的神经元。

回到卷积层，因为存在许多相同神经元的拷贝，所以许多权重值出现在多神经元中。

![](/image/understanding_convolutions/Conv-9-Conv2-XY-W.png)

其对应与等式：
<center>y0=σ(W0x0+W1x1−b)</center>
<center>y1=σ(W0x1+W1x2−b)</center>

所以，通常情况下，一个权重矩阵以不同的权重将每一个输入与神经元相连：

![](/image/understanding_convolutions/f7.png)

一个如上所示的卷积层权重矩阵中，相同的权值会出现在许多位置。而且因为神经元没有连接到许多可能的输入，所以其中有很多的零。

![](/image/understanding_convolutions/f8.png)

与上面的矩阵相乘等同于与` [...0,w1,w0,0...]`做卷积。滑动到不同位置的功能相当于在那些位置上具有神经元。

对于二维卷积层是什么情况呢？

![](/image/understanding_convolutions/Conv2-5x5-Conv2-XY.png)

二维卷积层的布线对应于二维卷积。

考虑我们使用卷积来检测图像中的边缘的例子，通过滑动内核并将其应用于图中的每一处。与其类似的，卷积层将神经元应用于输入的每一处。

### 结论
我们在这篇博文中介绍了很多的数学原理，虽然可能并不明显。 卷积显然是概率理论和计算机图形学中的有用工具，但是使用卷积来分析卷积神经网络能得到什么呢？

第一个优点是我们获得了一些非常强大的语言来描述神经网络的布线。 到目前为止，我们所处理的例子并不复杂，所以这个好处可能并不明显，但是卷积会使我们摆脱大量不愉快的布线记录。

其次，卷积具有显著的实施优势。 许多库提供高效的卷积程序。 此外，虽然卷积天然的是`O（n*n）`操作，但是使用一些相当深刻的数学理论，可以创建其`O（nlog（n））`的实现。 我们将在未来的一篇文章中详细讨论这个问题。

事实上，在GPU上使用高效的并行卷积实现，已经成为当今计算机视觉的基本要素。

### 此系列中的下一篇文章

这篇博文是卷积神经网络及其概括系列的一部分。 前两篇文章可能比较适合那些熟悉深度学习的人员进行阅读，而其后的博文应该是所有人都感兴趣的。 要获取更新，请订阅我的RSS Feed！

请在下面或旁边评论。 提交请求可以在github上进行。

### 致谢

我非常感谢Eliana Lorch，对其帮助广泛的讨论卷积和帮助撰写这篇文章。

我也要感谢Michael Nielsen和Dario Amodei的意见和支持。

<a name="comments1"></a>[1].我们想要第一次滚动距离为`a`，并且第二次滚动距离为`b`单位的概率。 概率分布`P（A）= f（a）`和`P（b）= g（b）`是相互独立的，两个分布都是以0为中心，所以`P(a,b)=P(a)∗P(b)=f(a)⋅g(b)`

<a name="comments2"></a>[2].我以前没有看到非标准定义，不过其似乎有很多好处。 在将来的博文中，我们将会发现这个定义非常有用，因为它适用于新的代数结构的泛化。 同时它也具有使得很多卷积的代数性质十分明显的优点。

例如，卷积满足交换律，即`f∗g=g∗f`,因为：

![](/image/understanding_convolutions/f9.png)

卷积也满足结合律，即`(f∗g)∗h=f∗(g∗h)(f∗g)∗h=f∗(g∗h)`，因为：

![](/image/understanding_convolutions/f10.png)

<a name="comments3"></a>[3].此处还有偏差，这是神经元是否触发的“门槛”，但是它更简单，我不想混淆这一节而去谈论它。

[understanding-convolutions]: http://colah.github.io/posts/2014-07-Understanding-Convolutions/
[example]: https://docs.gimp.org/en/plug-in-convmatrix.html
[eassay]: http://colah.github.io/posts/2014-07-Conv-Nets-Modular/

