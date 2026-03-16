import express from 'express';
import { authRouter } from './api/auth';
import { usersRouter } from './api/users';

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Hello from Backend!');
});

app.use('/auth', authRouter);
app.use('/users', usersRouter);

app.listen(port, () => {
  console.log(`Backend listening at http://localhost:${port}`);
});
