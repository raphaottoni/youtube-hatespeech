#!/usr/bin/env Rscript 
library(tidyverse)
library(stringr)
library(forcats)
library(magrittr)
library(viridis)

channels_names <- read.table("../../data/channels_names.tsv", header=TRUE, sep="\t") %>%
    mutate(channel_type = fct_recode(channel_type,
        "right-wing" = "altright",
        "baseline"     = "general"
    ))

# NOTE: arquivo weat.csv disponibilizado neste mesmo diretório
# Como o formato do arquivo não era "tidy", tive que fazer as 
# manipulações abaixo para deixá-lo num formato bom de se manipular
# Envio também o arquivo weat-full.csv, que é o arquivo gerado após
# a manipulação. Caso vc já gere a saida no formato weat-full.csv,
# pode ignorar toda essa manipulação.

df <- read.csv("../../data/weat.csv") %>%
    mutate(source = type) %>%
    select(-channel_type, -channel_name, -type) %>%
    gather(variable, value, -channel_id, -source) %>%
    mutate(variable_ok = str_replace_all(variable, "_([dp])$", "-\\1")) %>% 
    separate(variable_ok, into = c("bias", "metric_"), sep = "-") %>%
    mutate(metric = factor(if_else(metric_ == "p", "p.value", "D")),
           bias   = factor(bias)) %>%
    mutate(bias = fct_recode(bias,
        "Immigrants"  = "immigration",
        "Muslims"     = "religion",
        "LGBT people" = "sexuality"
    )) %>%
    select(channel_id, source, bias, metric, value) %>%
    spread(metric, value) %>%
    arrange(channel_id, bias, source)

write.table(df, "../../info/weat/weat-full.tsv", sep="\t", row.names=FALSE, quote=FALSE)

df %<>% left_join(channels_names) %>%
    mutate(channel_name = fct_reorder(channel_name, as.numeric(channel_type))) %>%
    mutate(source = fct_recode(source, "caption" = "transcript")) %>%
    mutate(source = fct_relevel(source, "caption", "comments"))

df_plot <- df %>%
    filter(channel_id != "wiki") %>%
    #mutate(fill = if_else(p.value <= 0.05, D, NaN)) %>%
    filter(p.value < 0.1) %>%
    #filter(p.value <= 0.06) %>%
    #filter(p.value <= 0.1) %>%

    mutate(p_cat = factor(if_else(p.value < 0.05, "< 0.05",
                          if_else(p.value < 0.10, "[0.05, 0.10)",
                                  "> 0.10")),
                          levels=c("< 0.05", "[0.05, 0.10)", "> 0.10"))) %>%
    mutate(D_cat = factor(if_else(D <=  0.20, "very small (-Inf, 0.2]",
                          if_else(D <=  0.50, "small (0.2, 0.5]",
                          if_else(D <=  0.80, "medium (0.5, 0.8]",
                          if_else(D <=  1.20, "large (0.8, 1.2]",
                          if_else(D <=  2.00, "very large (1.2, 2.0]", 
                                              "huge (2.0, Inf)"))))),
                          levels=c("very small (-Inf, 0.2]",
                                   "small (0.2, 0.5]",
                                   "medium (0.5, 0.8]",
                                   "large (0.8, 1.2]",
                                   "very large (1.2, 2.0]",
                                   "huge (2.0, Inf)")))

df_base <- df %>%
    filter(channel_id == "wiki") %>%
    select(-p.value, -channel_name, -channel_type)

df_diff <- df_plot %>%
    select(-p.value, -D_cat, -p_cat) %>%
    spread(source, D) %>%
    mutate(diff = comments - caption,
           y = (comments + caption)/2) %>%
    mutate(label = if_else(diff >= 0, sprintf("+ %.1f", diff), sprintf("- %.1f", -diff))) %>%
    select(-comments, -caption) %>%
    filter(!is.na(diff))

ggplot(df_plot, aes(x = bias, y = source, fill = D_cat)) +
    facet_grid(channel_type + channel_name~ ., switch="y", scales="free") +
    geom_tile() +
    geom_text(aes(label = round(D, 1))) +
    scale_x_discrete("Bias", position="top") +
    scale_y_discrete("Source") +
    #scale_fill_viridis(limits = c(0, 2)) +
    #scale_fill_gradientn(colours=viridis(6), limits = c(0, 2), breaks=c(0, 0.2, 0.5, 0.8, 1.2, 2.0)) +
    scale_fill_manual("Cohen's D", drop=FALSE, values=viridis(6)) +
    theme(strip.text.y = element_text(angle = 180),
          axis.text.x = element_text(angle = 45, hjust = 0))
ggsave("weat-matrix.pdf", device=cairo_pdf, width=8, height=14)

ggplot(df_plot, aes(x=D, y=channel_name, color=p_cat, shape=source)) +
    #facet_wrap(~ bias, nrow=1) +
    facet_grid(channel_type ~ bias, switch="y", scales="free_y", space="free") +
    geom_point(size=2) +
    geom_vline(data=df_base, aes(xintercept=D, linetype=source), color="darkmagenta") +
    geom_text(data=df_diff %>% mutate(source="caption"), aes(x=0.05, label=label), color="black", size=3) +
    scale_x_continuous("Effect Size", limits=c(0, 2)) +
    scale_y_discrete("Channel") +
    scale_color_brewer(name="p-value", palette="Dark2") +
    scale_linetype_manual(name = "reference", values = c("dashed"))+
    theme(legend.position="top")
ggsave("weat-points.pdf", device=cairo_pdf, width=10, height=5)

df_plot %>%
    filter(p.value < 0.05) %>%
    mutate(channel_type = fct_recode(channel_type, "right-w." = "right-wing",
                                                   "basel."   = "baseline")) %>%
    ggplot(aes(x=channel_type, y=D, fill=source)) +
        facet_wrap(~ bias, nrow=1, scales="free_y") +
        geom_boxplot() +
        geom_hline(data=df_base, aes(yintercept=D, linetype=source), color="darkmagenta") +
        scale_x_discrete("Channel Type") +
        scale_y_continuous("Effect Size") +
        scale_fill_brewer(palette="Set1") +
        scale_linetype_manual(name = "reference", values = c("dashed"))+
        theme(legend.position="top")
ggsave("weat-boxplot.pdf", device=cairo_pdf, width=5, height=2.5)

