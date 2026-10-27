import { Injectable, Logger, OnModuleInit } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import nodemailer, { type Transporter } from 'nodemailer';
import type { PropositoCodigo } from '../auth/entities/codigo-verificacion.entity.js';

const ASUNTO: Record<PropositoCodigo, string> = {
  verificar_correo: 'Tu código para verificar el correo — AdaptiveLearn',
  recuperar_contrasena: 'Tu código para recuperar la contraseña — AdaptiveLearn',
};

const PARA_QUE: Record<PropositoCodigo, string> = {
  verificar_correo: 'verificar tu correo en AdaptiveLearn',
  recuperar_contrasena: 'recuperar tu contraseña de AdaptiveLearn',
};

/**
 * Envío de los códigos por correo (nota R5 del docente). Usa SMTP con los
 * datos de .env: MAIL_HOST, MAIL_PORT, MAIL_USER, MAIL_PASSWORD, MAIL_FROM.
 * La cuenta del sistema es adaptivelearn.sistema@gmail.com (Gmail:
 * smtp.gmail.com, puerto 587, con una contraseña de aplicación). Ninguna
 * clave vive en el código.
 *
 * Sin MAIL_HOST (desarrollo), el código se escribe en la consola del
 * servidor, y se avisa al arrancar.
 */
@Injectable()
export class CorreoService implements OnModuleInit {
  private readonly logger = new Logger(CorreoService.name);
  private transporter: Transporter | null = null;
  private remitente = '';

  constructor(private readonly configService: ConfigService) {}

  onModuleInit(): void {
    const host = this.configService.get<string>('MAIL_HOST');
    if (!host) {
      this.logger.warn(
        'MAIL_HOST no está configurado: los códigos NO se envían por correo; ' +
          'se escriben en esta consola (solo para desarrollo).',
      );
      return;
    }
    const port = Number(this.configService.get<string>('MAIL_PORT') || 587);
    this.remitente =
      this.configService.get<string>('MAIL_FROM') ||
      this.configService.getOrThrow<string>('MAIL_USER');
    this.transporter = nodemailer.createTransport({
      host,
      port,
      // 465 es SMTP sobre TLS; 587 empieza en claro y sube a TLS (STARTTLS)
      secure: port === 465,
      requireTLS: port !== 465,
      auth: {
        user: this.configService.getOrThrow<string>('MAIL_USER'),
        pass: this.configService.getOrThrow<string>('MAIL_PASSWORD'),
      },
    });
    this.logger.log(`Correo configurado: SMTP ${host}:${port}, remitente ${this.remitente}`);
  }

  get configurado(): boolean {
    return this.transporter !== null;
  }

  async enviarCodigo(correo: string, codigo: string, proposito: PropositoCodigo): Promise<void> {
    if (!this.transporter) {
      this.logger.warn(`[DESARROLLO] Código para ${PARA_QUE[proposito]} (${correo}): ${codigo}`);
      return;
    }
    const texto =
      `Tu código para ${PARA_QUE[proposito]} es: ${codigo}\n\n` +
      'Vence en 10 minutos. Si no lo pediste, ignora este mensaje: nadie puede ' +
      'entrar a tu cuenta sin este código.\n';
    await this.transporter.sendMail({
      from: this.remitente,
      to: correo,
      subject: ASUNTO[proposito],
      text: texto,
    });
  }
}
