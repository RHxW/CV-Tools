import torch


class OptimizerWarmUpScheduler:
    # only support close form
    def __init__(self, optimizer, start_lr=0., warmup_strategy="linear", warmup_epoch=5, start_epoch=0):
        if not isinstance(optimizer, torch.optim.Optimizer):
            raise RuntimeError("optimizer is not 'torch.optim.Optimizer' class")
        self.optimizer = optimizer
        self.start_lr = start_lr
        self.end_lr = optimizer.defaults["lr"]
        if self.start_lr > self.end_lr:
            self.start_lr = 0.

        self.warmup_epoch = warmup_epoch
        self.cur_epoch = start_epoch

        self.warmup_strategy = warmup_strategy
        if self.warmup_strategy == "linear":
            self.lr_schedule = self._get_lr_schedule_linear()
        # elif self.warmup_strategy == "exponential":  # TODO
        #     pass
        else:
            print("set warmup_strategy to default: 'linear'")
            self.warmup_strategy = "linear"
            self.lr_schedule = self._get_lr_schedule_linear()

    def step(self):
        if self.cur_epoch >= self.warmup_epoch:
            return
        lr = self.lr_schedule[self.cur_epoch]
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr
        self.cur_epoch += 1

    def _get_lr_schedule_linear(self):
        lr_step = (self.end_lr - self.start_lr) / (self.warmup_epoch - self.cur_epoch)
        lr_schedule = []
        for i in range(self.cur_epoch, self.warmup_epoch):
            lr_schedule.append(round((i + 1) * lr_step, 6))
        return lr_schedule

    def _get_lr_schedule_exponential(self):
        pass


if __name__ == "__main__":
    net = torch.nn.Conv2d(3, 5, 3)
    optimizer = torch.optim.SGD(params=net.parameters(), lr=0.001)
    warmup_scheduler = OptimizerWarmUpScheduler(optimizer, warmup_epoch=10)
    print(111)
