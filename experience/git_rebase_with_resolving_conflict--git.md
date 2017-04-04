# git_rebase_with_resolving_conflict--git

命令行内解决rebase conflict
## 进行Rebase时，遇到conflict
当我们执行操作git rebase somebranch时，有可能遇到冲突，冲突的文件中会包含以下内容：
```
<<<<<<< HEAD
Creating a new branch is quick & simple.
=======
Creating a new branch is quick AND simple.
>>>>>>> somebranch
```
握草，什么鬼，怎么又有冲突，要吓死宝宝吗？回退吗？直接用merge算了？

这个时候，不能屈服，一定不要屈服，不就是冲突么，只是个小boss。

## 解决冲突前的概念
在<<<<<<< HEAD和=======之间的是我们当前分支的内容，为ours
在======= 和>>>>>>> feature1之间的是somebranch上面对应的内容,为theirs

## 那么如何解决冲突呢？

1. 确定内容该如何修改，`git diff`,有三种情况：
    1. 使用我们当前的
    2. 使用somebranch分支上面的
    3. 两个都需要。

2. 内容修改:
    1. 使用我们当前的内容，执行 `git checkout --ours conflict-file-name`
    2. 使用somebranch分支上面的内容，执行`git checkout --theirs conflict-file-name`
    3. 如果都需要使用，则`vim confict-file-name`,直接编辑冲突文件，修改之后直接`wq`退出编辑。

3. 执行 `git add .`
4. `git rebase --continue`
    如果执行之后没有成功，有其他提示，按照提示`git rebase --skip`执行进行即可。
5. 擦亮眼睛，我去，怎么还没有弄好！？ 
6. 淡定，重复1至4步，直到返回正常分支。
7. 大功告成，舒坦！！！呼......


